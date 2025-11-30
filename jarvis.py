import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import wikipedia
import webbrowser
import random
import subprocess
import google.generativeai as genai


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

# print(voices[0]) # There are two types of Voice id. 1st voice id: male
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


def play_music():
        music_dir = "D:\\Data_Science_and_Machine_Learning\\03-Inceptionbd\\14-(Module-14)_Mega_Project_(Python)\\Class_Practices\\jarvis_system_first_part\\JARVIS-Voice-Assistant-System\\music"
        try:
            surah = os.listdir(music_dir)
            if surah:
                random_surah = random.choice(surah)
                speak(f"Playing a random surah: {random_surah}")
                os.startfile(os.path.join(music_dir, random_surah))
            else:
                speak("No music files found in your music directory.")
        except Exception:
            print("Sorry sir, I could not find your music folder.")


def gemini_model_response(user_input):
    GEMINI_API_KEY = "Your API KEY"
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Your name is JARVIS, You act like JARVIS. Answer the provided questions in short: {user_input}"
    response = model.generate_content(prompt)
    result = response.text

    return result


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

    elif "Who created you?" in query:
        speak("I was created by Asadul Islam sir.")

    elif "Thank you" in query:
        speak("It's my pleasure sir, Always happy to help.")
        logging.info("User expressed gratitude")

    elif "open google" in query:
        speak("Ok sir, Please type here what do you want to search")
        webbrowser.open("google.com")
        logging.info("User requested to open google")

    # open calculator
    elif "open calculator" in query or "calculator" in query:
        speak("Opening calculator...")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open calculator")

    # open Notepad
    elif "open notepad" in query:
        speak("Opening notepad...")
        subprocess.Popen("notepad.exe")
        logging.info("User requested to open notepad")

    # open terminal
    elif "open terminal" in query or "open cmd" in query:
        speak("Opening command prompt terminal...")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open terminal")

    # open calendar
    elif "open calendar" in query:
        speak("Opening calendar...")
        webbrowser.open("https://calendar.google.com")
        logging.info("User requested to open calendar")

    # Youtube search
    elif "open youtube" in query:
        speak("Opening youtube for you...")
        query = query.replace("youtube", "")
        webbrowser.open(f"https://www.youtube.com/results?query_search={query}")
        logging.info("User requested to open youtube")

    # Facebook
    elif "open facebook" in query:
        speak("Opening facebook for you...")
        webbrowser.open("facebook.com")
        logging.info("User requested to open facebook")

    elif "open github" in query:
        speak("Opening github for you...")
        webbrowser.open("github.com")
        logging.info("User requested to open github")

    elif "joke" in query:
        jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs."
                "What do you call a programmer without a girlfriend? A full-stack developer."
                "Why do Java developers wear glasses? Because they don't C#"
            ]
        speak(random.choice(jokes))

    elif "wikipedia" in query:
        speak("Searching wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia.")
        speak(results)
        logging.info("User requested information from wikipedia")

    elif "play music" in query or "music" in query:
        play_music()

    elif "exit" in query or "stop" in query:
        print("Thank you sir for your time. Have a great day!")
        logging.info("User exited the program")
        exit()

    else:
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for others questions")
