import cv2
import os

# Ensure 'samples' directory exists
os.makedirs("engine/auth/samples", exist_ok=True)

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # Width
cam.set(4, 480)  # Height

if not cam.isOpened():
    print("❌ Error: Could not open the webcam. Exiting...")
    exit()

print("✅ Webcam successfully opened!")

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_id = input("Enter a numeric user ID (e.g., 7 for aarav, 8 for pranav): ")

print("Taking samples, look at the camera... ")
count = 0  # Face sample count

while True:
    ret, img = cam.read()
    if not ret:
        print("❌ Error: Could not capture image. Exiting...")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))

    print(f"🔍 Detected {len(faces)} faces")  # Debugging

    for (x, y, w, h) in faces:
        count += 1
        filename = f"engine/auth/samples/face.{face_id}.{count}.jpg"
        cv2.imwrite(filename, gray[y:y+h, x:x+w])
        print(f"✅ Image saved: {filename}")  # Debugging

        # Draw a rectangle
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, f"Sample {count}/100", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('Face Sample Capture', img)

    if cv2.waitKey(100) & 0xff == 27 or count >= 100:  # Press 'ESC' or take 100 samples
        break

print("✅ Samples taken successfully. Closing...")
cam.release()
cv2.destroyAllWindows()
