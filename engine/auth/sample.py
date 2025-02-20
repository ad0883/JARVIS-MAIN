import cv2

# Create a video capture object to capture videos through the webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # Set video frame width
cam.set(4, 480)  # Set video frame height

# Load Haar cascade classifier for face detection
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_id = input("Enter a numeric user ID here (e.g., 7 for aarav, 8 for pranav): ")

print("Taking samples, look at the camera... ")
count = 0  # Initializing sample face count

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to capture image. Exiting.....")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        count += 1
        # Save the captured image in the 'samples' directory
        cv2.imwrite(f"engine\\auth\\samples\\face.{face_id}.{count}.jpg", gray[y:y+h, x:x+w])

        # Draw a rectangle around the detected face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, f"Sample {count}/100", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # Press 'ESC' to stop
        break
    elif count >= 100:  # Take 100 samples (More samples = Higher accuracy)
        break

print("Samples taken successfully. Closing the program...")
cam.release()
cv2.destroyAllWindows()
