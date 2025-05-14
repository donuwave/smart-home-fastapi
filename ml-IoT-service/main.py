from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

# RTSP‑адрес вашей камеры
STREAM_URL = 'rtsp://admin:Lfybbk1412200!@192.168.0.103:554/Streaming/Channels/101'

def gen_frames():
    """Читает кадры из RTSP и отдает их как части MJPEG."""
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        # Если не удалось подключиться — прерываем генератор
        raise RuntimeError("Не удалось открыть RTSP‑поток")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Кодируем кадр в JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()

            # yield в формате multipart/x-mixed-replace
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
            )
    finally:
        cap.release()

@app.get("/video_feed")
def video_feed():
    try:
        return StreamingResponse(
            gen_frames(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    except RuntimeError as e:
        # Если камера недоступна — вернем 503
        raise HTTPException(status_code=503, detail=str(e))
