import os
import eel
import subprocess
import time
from video_player import play_video  # Import the updated video player

from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")

            # 🎬 Play Video Instead (Now in Fullscreen)
            play_video()  

            speak("JARVIS at your service")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)

if __name__ == "__main__":
    start()
