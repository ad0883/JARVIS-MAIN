import os
from shlex import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if not search_term:
        speak("I couldn't understand what to play on YouTube. Please try again.")
        return
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)


microphone_in_use = False

def hotword():
    global microphone_in_use
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Initialize Porcupine with pre-trained keywords
        porcupine = pvporcupine.create(
            access_key="UrtVZgF00vg7ccv+KyzZtnIwJpikMM0t+C76Zi/cyxgVhecoZw2VVg==",  # Replace with your actual access key
            keywords=["jarvis"]
        )
        print("Hotword detection initialized successfully.")

        # Initialize PyAudio
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotword...")
        while True:
            if not microphone_in_use:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                print("Audio data captured.")  # Debug statement
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                print(f"Keyword index: {keyword_index}")  # Debug statement
                if keyword_index >= 0:
                    print("Hotword detected!")
                    microphone_in_use = True
                    from engine.command import takecommand
                    takecommand()  # Start listening for a command after hotword detection
                    microphone_in_use = False

    except Exception as e:
        print(f"Error in hotword detection: {e}")
    finally:
        # Safely clean up resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        if not results:
            speak("Contact not found in your address book.")
            return 0, 0

        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+'):
            mobile_number_str = '+91' + mobile_number_str  # Default to +91 if no country code
        return mobile_number_str, query
    except Exception as e:
        speak(f"Error finding contact: {e}")
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            target_tab = 12
            jarvis_message = f"Message sent successfully to {name}"
        elif flag == 'call':
            target_tab = 7
            message = ''
            jarvis_message = f"Calling {name}"
        else:
            target_tab = 6
            message = ''
            jarvis_message = f"Starting video call with {name}"

        # Encode the message for URL
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

        # Open WhatsApp with the constructed URL
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True, check=True)
        time.sleep(5)

        # Navigate tabs and send the message
        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')

        speak(jarvis_message)
    except Exception as e:
        speak(f"Failed to send WhatsApp message: {e}")

# chat bot 
def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except FileNotFoundError:
        speak("Chatbot configuration file is missing.")
    except Exception as e:
        speak(f"Error in chatbot: {e}")

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)