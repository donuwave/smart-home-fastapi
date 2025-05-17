import face_recognition
import os
import pickle

KNOWN_FACES_DIR = 'known_faces'
encodings_data = []

for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        encodings_data.append({
            'name': os.path.splitext(filename)[0],
            'encoding': encodings[0]
        })

with open('face_encodings.pkl', 'wb') as f:
    pickle.dump(encodings_data, f)

print("Готово! Энкодинги сохранены.")
