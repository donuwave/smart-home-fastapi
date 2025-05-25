import asyncio
import time
from dataclasses import dataclass, field
from typing import List

import cv2
import numpy as np
import face_recognition
from starlette.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from api_v1.device.repository import DeviceRepository
from api_v1.face.repository import FaceRepository
from api_v1.stream.schema import PushParams
from config.broker import connection_broker


@dataclass
class StreamService:
    device_repository: DeviceRepository
    face_repository: FaceRepository

    process_every_n_frames: int = 10
    encoding_tolerance: float = 0.45
    resize_scale: float = 0.25
    reload_interval_s: float = 60.0
    notification_interval_s: float = 60.0
    clear_unknown_interval_s: float = 3600.0

    _unknown_encodings: List[List[float]] = field(default_factory=list, init=False)
    _known_encodings: List[List[float]] = field(default_factory=list, init=False)
    _known_names: List[str] = field(default_factory=list, init=False)
    _pending_unknown_cnt: int = field(default=0, init=False)
    _last_notify: float = field(default=0.0, init=False)
    _last_clear_unknown: float = field(default=0.0, init=False)
    _last_reload: float = field(default=0.0, init=False)

    async def raw_video_feed(self, device_id: int) -> StreamingResponse:
        device = await self.device_repository.get_item_device_in_home(device_id=device_id)
        if not device:
            raise RuntimeError(f"Устройство {device_id} не найдено")
        stream_url = device.full_address

        return StreamingResponse(
            self._raw_frame_generator(stream_url),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    async def _raw_frame_generator(self, stream_url: str):
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            raise RuntimeError("Не удалось открыть RTSP-поток")
        try:
            while True:
                success, frame = await run_in_threadpool(cap.read)
                if not success:
                    break
                ret, buf = await run_in_threadpool(cv2.imencode, '.jpg', frame)
                if not ret:
                    continue
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    buf.tobytes() +
                    b'\r\n'
                )
        finally:
            cap.release()

    async def video_feed(self, home_id: int, device_id: int) -> StreamingResponse:
        device = await self.device_repository.get_item_device_in_home(
            device_id=device_id
        )

        if not device:
            raise RuntimeError(f"Устройство {device_id} не найдено")
        stream_url = device.full_address

        await self._reload_embeddings(home_id)

        return StreamingResponse(
            self._frame_generator(stream_url, home_id),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    async def _reload_embeddings(self, home_id: int):
        faces = await self.face_repository.get_item_face_by_home_id(home_id=home_id)
        self._known_encodings = [f.embedding for f in faces]
        self._known_names = [f.name      for f in faces]
        self._last_reload = time.monotonic()
        print(f"🔄 Перезагружено {len(self._known_encodings)} эмбеддингов")

    async def _frame_generator(self, stream_url: str, home_id: int,):
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            raise RuntimeError("Не удалось открыть RTSP-поток")

        frame_count = 0

        try:
            while True:
                success, frame = await run_in_threadpool(cap.read)
                if not success:
                    break

                frame_count += 1

                now = time.monotonic()
                if now - self._last_reload >= self.reload_interval_s:
                    await self._reload_embeddings(home_id)

                if now - self._last_clear_unknown >= self.clear_unknown_interval_s:
                    self._unknown_encodings.clear()
                    self._pending_unknown_cnt = 0
                    self._last_clear_unknown = now
                    print("🗑️ Кэш незнакомцев очищен")

                if frame_count % self.process_every_n_frames == 0:
                    messages = await self._detect_and_track(frame, home_id)
                    for msg in messages:
                        print(msg)

                ret, buf = await run_in_threadpool(cv2.imencode, '.jpg', frame)
                if ret:
                    chunk = buf.tobytes()
                    yield (
                        b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' +
                        chunk +
                        b'\r\n'
                    )
        finally:
            cap.release()


    async def _detect_and_track(self, frame, home_id: int) -> List[str]:
        msgs: List[str] = []
        small = cv2.resize(frame, (0, 0), fx=self.resize_scale, fy=self.resize_scale)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locs = face_recognition.face_locations(rgb_small)
        embs = face_recognition.face_encodings(rgb_small, locs)
        now = time.monotonic()

        for emb in embs:
            if self._known_encodings:
                d_known = face_recognition.face_distance(self._known_encodings, emb)
                if np.min(d_known) < self.encoding_tolerance:
                    continue

            if self._unknown_encodings:
                d_unknown = face_recognition.face_distance(self._unknown_encodings, emb)
                if np.min(d_unknown) < self.encoding_tolerance:
                    continue

            self._unknown_encodings.append(list(emb))
            self._pending_unknown_cnt += 1
            msgs.append("⚠️ Обнаружен новый незнакомый человек!")

        if self._pending_unknown_cnt > 0 and (now - self._last_notify) >= self.notification_interval_s:
            await self._push_notification_all_session_by_id(home_id=home_id)

            print(f"🔔 Уведомление: за последнюю минуту {self._pending_unknown_cnt} новых незнакомцев")
            self._pending_unknown_cnt = 0
            self._last_notify = now

        return msgs

    async def _push_notification_all_session_by_id(self, home_id: int):
        body = {
            "key": "session.get_list_session_by_home_id",
            "body": home_id
        }

        session_list = await connection_broker(
            queue_name="auth_queue",
            queue_name_callback="callback_auth_queue",
            body=body
        )

        for sess in session_list:
            token = sess.get("fcm_token")
            if not token:
                continue

            push_params = PushParams(
                token=token,
                title="⚠️ Обнаружен новый незнакомец",
                body="Проверьте камеру"
            )
            push_body = {
                "key": "notification.send_push",
                "body": dict(push_params)
            }
            await connection_broker(
                queue_name="notification_queue",
                queue_name_callback="callback_notification_queue",
                body=push_body
            )


    async def start_processing(
            self,
            home_id: int,
            device_id: int
    ):
        device = await self.device_repository.get_item_device_in_home(device_id=device_id)
        if not device:
            print(f"[StreamService] Камера {device_id} не найдена — пропускаем")
            return
        stream_url = device.full_address
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print(f"[StreamService] Не удалось открыть поток {stream_url}")
            return

        await self._reload_embeddings(home_id)

        frame_count = 0
        try:
            while True:
                success, frame = await run_in_threadpool(cap.read)
                if not success:
                    break
                frame_count += 1

                now = time.monotonic()
                if now - self._last_reload >= self.reload_interval_s:
                    await self._reload_embeddings(home_id)
                if now - self._last_clear_unknown >= self.clear_unknown_interval_s:
                    self._unknown_encodings.clear()
                    self._pending_unknown_cnt = 0
                    self._last_clear_unknown = now

                if frame_count % self.process_every_n_frames == 0:
                    msgs = await self._detect_and_track(frame, home_id=home_id)
                    for m in msgs:
                        print(f"[StreamService] {m}")

                await asyncio.sleep(0)
        finally:
            cap.release()
            print(f"[StreamService] Background-стрим камеры {device_id} остановлен.")