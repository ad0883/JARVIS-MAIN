import cv2
import numpy as np
import os

# Path for face samples
samples_path = "engine/auth/samples"
trainer_path = "engine/auth/trainer/trainer.yml"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Create LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=50)

# Function to get the face samples and corresponding IDs
def get_images_and_labels(samples_path):
    image_paths = [os.path.join(samples_path, f) for f in os.listdir(samples_path) if f.endswith(".jpg")]
    face_samples = []
    ids = []

    for image_path in image_paths:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = img[y:y + h, x:x + w]
            face_resized = cv2.resize(face, (200, 200))  # Resize for consistency
            face_samples.append(face_resized)
            
            # Extract ID from the filename (e.g., "face.7.1.jpg" → ID = 7)
            id = int(os.path.split(image_path)[-1].split(".")[1])
            ids.append(id)

    return face_samples, ids

print("Training faces. Please wait...")

faces, ids = get_images_and_labels(samples_path)

if len(faces) == 0:
    print("No face samples found. Please capture samples first.")
else:
    # Train the recognizer
    recognizer.train(faces, np.array(ids))

    # Save the trained model
    recognizer.save(trainer_path)
    print(f"Training complete. Model saved as {trainer_path}.")
