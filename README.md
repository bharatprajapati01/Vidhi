# VIDHI – Voice Intelligent Digital Helper Interface

VIDHI is a Python-based voice assistant that continuously listens to user commands without requiring a wake word. It can perform multiple tasks like telling time, playing music, setting reminders, taking notes, fetching weather, news, and more.

---

## 🚀 Features

- 🎤 Voice Recognition (always listening)
- 🔊 Text-to-Speech response (female voice)
- ⏰ Time and Date information
- 🌐 Open websites (YouTube, Google)
- 🎵 Play songs on YouTube
- 🧮 Basic calculator (safe evaluation)
- ⏳ Set reminders (with background thread)
- 📝 Save and read notes
- 🌦️ Get weather updates
- 📰 Fetch latest news headlines
- 📚 Wikipedia search

---

## 📁 Project Files

- main.py → Main program file
- vidhi_reminders.json → Stores reminders
- vidhi_notes.json → Stores notes

---

## ⚙️ Requirements

Install the following Python libraries before running:
pip install pyttsx3
pip install SpeechRecognition
pip install pywhatkit
pip install requests
pip install wikipedia

---

🧠 How It Works
The assistant continuously listens using your microphone.
It converts speech to text using Google Speech Recognition.
Based on keywords, it performs specific tasks.
It responds back using text-to-speech.

💡 Example Commands
"What is the time"
"Open YouTube"
"Play Arijit Singh songs"
"Calculate 5 + 10"
"Remind me in 2 minutes to study"
"Remember that I have an exam tomorrow"
"Read my notes"
"Weather in Delhi"
"Tell me about Python"

🔐 Notes
Internet connection is required for:
Speech recognition
Weather updates
News
Wikipedia
Reminders and notes are saved locally in JSON files.

👨‍💻 Author

Bharat Prajapati
