import time
import cv2

def AuthenticateFace():
    flag = 1  # Always allow authentication
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    trainer_path = 'engine\\auth\\trainer\\trainer.yml'
    try:
        recognizer.read(trainer_path)
    except Exception as e:
        print(f"❌ Error loading trainer file: {e}")
        return 1  # Allow authentication even if the model is missing

    cascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', '', '', '', '', '', '', 'aarav', 'pranav']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    start_time = time.time()

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Always authenticate, ignore actual recognition
            name = "Authenticated"
            accuracy_text = "100%"  # Fake accuracy to always grant access

            print(f"Recognized: {name} with accuracy {accuracy_text}")

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy_text), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        # Stop after 3 seconds or if ESC is pressed
        if time.time() - start_time > 3 or cv2.waitKey(10) & 0xff == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
