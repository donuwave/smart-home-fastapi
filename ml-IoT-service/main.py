from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import face_recognition
import pickle

app = FastAPI()

STREAM_URL = 'rtsp://admin:Lfybbk1412200!@192.168.0.103:554/Streaming/Channels/101'

with open('face_encodings.pkl', 'rb') as f:
    encodings_data = pickle.load(f)

known_face_encodings = [d['encoding'] for d in encodings_data]
known_face_names = [d['name'] for d in encodings_data]

print(f"Известные лица: {len(known_face_encodings)}")

def gen_frames():
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть RTSP‑поток")

    frame_count = 0
    process_every_n_frames = 10  # Проверять 1 раз в 10 кадров

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame_count += 1
            if frame_count % process_every_n_frames == 0:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                print('Детектим лица')
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
                    print('Нашел лицо!')
                    if not any(matches):
                        print("⚠️ Неопознанное лицо обнаружено!")
                    else:
                        print("Знакомое лицо!!!")

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()

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
        raise HTTPException(status_code=503, detail=str(e))
