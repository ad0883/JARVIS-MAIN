import cv2
import os
import pygame
import threading

VIDEO_PATH = "static/startup.mp4"
AUDIO_PATH = "static/startup.mp3"

def play_sound():
    """Plays audio using pygame."""
    pygame.init()
    pygame.mixer.init()

    if not os.path.exists(AUDIO_PATH):
        print(f"❌ Error: Audio file '{AUDIO_PATH}' not found!")
        return
    
    pygame.mixer.music.load(AUDIO_PATH)
    pygame.mixer.music.play()

def play_video(video_path=VIDEO_PATH):
    """Plays video in fullscreen mode with sound."""
    if not os.path.exists(video_path):
        print(f"❌ Error: File '{video_path}' not found!")
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file '{video_path}'.")
        return

    # Start playing sound in a separate thread
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.start()

    # Open video in fullscreen
    window_name = "JARVIS Startup"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("✅ Video finished playing.")
            break

        cv2.imshow(window_name, frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to close
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()  # Stop pygame audio

