import multiprocessing
import time
import subprocess
# To run Jarvis
def startJarvis():
    print("Jarvis process is running.")
    from main import start
    start()

# To run hotword detection
def listenHotword():
    print("Hotword detection process is running.")
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    # Start both processes
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)

    p1.start()
    p2.start()

    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stopped.")