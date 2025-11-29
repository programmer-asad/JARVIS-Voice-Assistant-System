import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import wikipedia
import webbrowser
import random
import subprocess


# Logging configuration

LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"


os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# Activating voice from our system

engine = pyttsx3.init("sapi5")
engine.setProperty('rate', 200)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

    # print(voices[0]) # There are two types of Voice id. this is first voice id: male
    # print(voices[1]) # 2nd voice id, female


# This is speak function

def speak(text):
    """ This function converts text to voice
    Args:
        text
    returns:
        voice 
    """
    engine.say(text)
    engine.runAndWait()


# speak("Hello! My name is Abu Talha")


# This function recognize the speech and converts it to text


def takeCommand():
    """ This function takes command and recognize
    Returns:
        text as query
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        logging.info(e)
        print("Please say again.")
        return "None"
    return query


def greeting():
    hour = (datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good morning sir, How are you doing?")

    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon sir, How are you doing?")

    else:
        speak("Good Evening sir, How are you doing?")

    speak("I am Jarvis. Please tell me how may I help you today?")


greeting()


while True:
    query = takeCommand().lower()
    print(query)

    if "your name" in query:
        speak("My name is Jarvis")
        logging.info("User ask for assistant's name.")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir time is {strTime}")
        logging.info("User asked for the current time")

    # small talk
    elif "how are you" in query:
        speak("I am functioning at full capacity sir.")

    elif "Who made you" in query:
        speak("I was created by Asadul Islam sir.")

    elif "Thank you" in query:
        speak("It's my pleasure sir, Always happy to help.")

    elif "open google" in query:
        speak("Ok sir, Please type here what do you want to search")
        webbrowser.open("google.com")

    elif "exit" in query:
        print("Thank you sir for your time. Have a great day!")
        logging.info("User exited the program")
        exit()

    else:
        print("I am sorry, I can't help you with that")
        logging.info("User asked for unsupported command")
