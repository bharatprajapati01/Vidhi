"""
VIDHI – Voice Intelligent Digital Helper Interface
Always listening voice assistant (no wake word)
"""
import ast
import datetime
import json 
import operator
import os
import threading
import time
import webbrowser
import re
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
REMINDER_FILE = "vidhi_reminders.json"
NOTES_FILE = "vidhi_notes.json"
NEWS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
# --------------------------------------------------
# TTS ENGINE
# --------------------------------------------------
def speak(text):
    try:
        engine = pyttsx3.init()  
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        text = f"Chief, {text}"
        print("VIDHI ->", text)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("TTS Error:", e)


# --------------------------------------------------
# SPEECH RECOGNITION
# --------------------------------------------------
recognizer = sr.Recognizer()
wikipedia.set_lang("en")
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio).lower()
        print("YOU ->", query)
        return query
    except:
        speak("Sorry, I did not catch that")
        return ""
# --------------------------------------------------
# SAFE CALCULATOR
# --------------------------------------------------
def safe_calc(expr):
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError
    node = ast.parse(expr, mode="eval").body
    return _eval(node)
# --------------------------------------------------
# REMINDERS
# --------------------------------------------------
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE) as f:
            return json.load(f)
    return []
def save_reminders(r):
    with open(REMINDER_FILE, "w") as f:
        json.dump(r, f)
def reminder_daemon():
    while True:
        now = time.time()
        reminders = load_reminders()
        for r in reminders[:]:
            if r["t"] <= now:
                speak(f"Reminder: {r['msg']}")
                reminders.remove(r)
        save_reminders(reminders)
        time.sleep(10)
threading.Thread(target=reminder_daemon, daemon=True).start()
# --------------------------------------------------
# NOTES / MEMORY
# --------------------------------------------------
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE) as f:
            return json.load(f)
    return []
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)
# --------------------------------------------------
# NEWS
# --------------------------------------------------
def get_news():
    try:
        import xml.etree.ElementTree as ET
        xml = requests.get(NEWS_URL).text
        root = ET.fromstring(xml)
        headlines = [item.find("title").text for item in root.iter("item")][:5]
        return "Top news: " + "; ".join(headlines)
    except:
        return "News service unavailable"
# --------------------------------------------------
# WIKIPEDIA
# --------------------------------------------------
def tell_wikipedia(query):
    for p in ("who is", "what is", "tell me about"):
        query = query.replace(p, "")
    try:
        return wikipedia.summary(query.strip(), sentences=2, auto_suggest=False)
    except:
        return "No information found"
# --------------------------------------------------
# MAIN ASSISTANT
# --------------------------------------------------
def assistant():
    speak("Hello, I am VIDHI, your virtual voice assistant")
    while True:
        query = listen()
        if not query:
            continue
        # EXIT
        if "exit" in query or "quit" in query:
            speak("Goodbye")
            break
        # TIME / DATE
        elif "time" in query:
            speak(datetime.datetime.now().strftime("%H:%M:%S"))
        elif "date" in query:
            speak(datetime.datetime.now().strftime("%d %B %Y"))
        # OPEN
        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")
        # PLAY MUSIC
        elif "play" in query:
            speak("Playing on YouTube")
            pywhatkit.playonyt(query.replace("play", ""))
        # CALCULATOR
        elif "calculate" in query:
            try:
                result = safe_calc(query.replace("calculate", "").strip())
                speak(f"The answer is {result}")
            except:
                speak("Unable to calculate")
        # REMINDER
        elif "remind me" in query and "in" in query:
            try:
                parts = query.split()
                i = parts.index("in")
                minutes = int(parts[i + 1])
                msg = " ".join(parts[i + 2:])
                reminders = load_reminders()
                reminders.append({"t": time.time() + minutes * 60, "msg": msg})
                save_reminders(reminders)
                speak("Reminder set")
            except:
                speak("Could not set reminder")
        # NOTES FEATURE
        elif "remember that" in query:
            note = query.replace("remember that", "").strip()
            if note:
                notes = load_notes()
                notes.append(note)
                save_notes(notes)
                speak("I have saved that")
            else:
                speak("What should I remember")
        elif "read my notes" in query:
            notes = load_notes()
            if notes:
                speak("Here are your notes")
                for n in notes:
                    speak(n)
            else:
                speak("You have no notes")
        elif "clear my notes" in query:
            save_notes([])
            speak("All notes deleted")
        # NEWS
        elif "news" in query:
            speak(get_news())
        # WIKIPEDIA
        elif any(x in query for x in ("who is", "what is", "tell me about")):
            speak(tell_wikipedia(query))
        else:
            speak("Sorry, I did not understand")
# --------------------------------------------------
# RUN
# --------------------------------------------------
assistant()
