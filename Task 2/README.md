# Task 2: Chatbot

This project showcases **three different chatbot implementations** developed in Python using GPT-powered responses via the `g4f` API. Each bot is uniquely styled and serves different purposes — from emotional conversations to direct AI FAQs and simple command-line queries.

---

## 📁 Files Overview

### 1. `AI_FAQs Bot.py` – Smart FAQ Chatbot
- Built using **Tkinter GUI**.
- Uses **text similarity + GPT** to answer frequently asked questions.
- Features:
  - Custom question/answer set
  - Voice output using `pyttsx3`
  - Search-based matching for best response
- Ideal for: 📚 Educational assistants, company FAQs, support bots

---

### 2. `Bestiebot.py` – Emotional Bestie Chatbot
- A full **emotional GUI chatbot** built with Tkinter.
- Responds with warmth, humor, and friendly tone.
- Features:
  - 🎨 Colorful UI with random themes
  - 🎤 Speech input + 🔊 Voice output
  - 💬 GPT-powered casual and kind replies
- Ideal for: 🧠 Mental health tools, companion bots, friendly assistants

---

### 3. `chatbot.py` – Minimal Command-Line Chatbot
- Simple Python console chatbot using GPT.
- Features:
  - Clean terminal interface
  - GPT-4/GPT-3.5 response engine
  - 🔊 Text-to-speech output
- Ideal for: Developers testing GPT logic, CLI users

---

## 🔧 Requirements

Install these before running:

```bash
pip install g4f pyttsx3 SpeechRecognition
