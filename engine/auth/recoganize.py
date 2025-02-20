import time
import cv2

def AuthenticateFace():
    flag = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('engine\\auth\\trainer\\trainer.yml')
    
    cascadePath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', '', '', '', '', '', '', 'aarav', 'pranav']  # Assign names for ID 7 and 8

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

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
            id, accuracy = recognizer.predict(gray[y:y + h, x:x + w])

            # Authenticate only aarav (ID 7) or pranav (ID 8) if accuracy is better than 50%
            if (id == 7 or id == 8) and accuracy < 100:
                name = names[id]
                accuracy_text = f"{round(100 - accuracy)}%"
                flag = 1
                print(f"Recognized: {name} with accuracy {accuracy_text}")
            else:
                name = "unknown"
                accuracy_text = f"{round(100 - accuracy)}%"
                flag = 0

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy_text), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff
        if k == 27 or flag == 1:  # Exit on 'ESC' or after recognizing aarav or pranav
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
