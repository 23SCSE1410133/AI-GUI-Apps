import tkinter as tk
from tkinter import ttk
import threading
import pyttsx3
import speech_recognition as sr
import random
import g4f

# Initialize TTS engine once globally
engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Speak function (Fixed)
def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# Get GPT response using g4f
def get_gpt_response(prompt):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": "You're an emotionally intelligent best friend. Respond with warmth, empathy, and a friendly tone."},
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        return f"⚠️ Chatbot Error: {str(e)}"

# Speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, user_input)
            handle_chat()
        except Exception:
            status_label.config(text="⚠️ Could not recognize speech.")

# Handle chat and bot reply
def handle_chat():
    user_text = entry.get().strip()
    if not user_text:
        return

    chat_history.config(state="normal")
    chat_history.insert(tk.END, f"You: {user_text}\n", 'user')
    chat_history.config(state="disabled")
    entry.delete(0, tk.END)

    def respond():
        bot_response = get_gpt_response(user_text)

        chat_history.config(state="normal")
        chat_history.insert(tk.END, f"BestieBot: {bot_response}\n", 'bot')

        # Speak Button (FIXED)
        def speak_response():
            speak(bot_response)

        speak_button = tk.Button(chat_history, text="🔊 Speak", font=("Comic Sans MS", 10, "bold"),
                                 bg="#FFD700", activebackground="#FFECB3",
                                 command=speak_response)
        chat_history.window_create(tk.END, window=speak_button)
        chat_history.insert(tk.END, "\n")

        chat_history.config(state="disabled")
        chat_history.see(tk.END)
        speak(bot_response)  # Optional auto speak

    threading.Thread(target=respond).start()

# GUI setup
root = tk.Tk()
root.title("🌈 BestieBot - Your Colorful Emotional Companion")
root.geometry("800x700")
root.minsize(500, 500)
root.resizable(True, True)

# Theme colors
colors = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7"]
chosen_colors = random.sample(colors, 3)
root.config(bg=chosen_colors[0])

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Comic Sans MS", 12), padding=6)

frame = tk.Frame(root, bg=chosen_colors[1])
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_history = tk.Text(frame, wrap=tk.WORD, bg="#fdf6e3", fg="#002b36", font=("Comic Sans MS", 13))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_history.config(state="disabled")
chat_history.tag_config('user', foreground=chosen_colors[2], font=("Comic Sans MS", 13, "bold"))
chat_history.tag_config('bot', foreground="#6B5B95", font=("Comic Sans MS", 13))

entry_frame = tk.Frame(root, bg=chosen_colors[0])
entry_frame.pack(pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Comic Sans MS", 14), bg="#e0f7fa")
entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

send_btn = tk.Button(entry_frame, text="Send 💌", command=handle_chat, font=("Comic Sans MS", 12, "bold"),
                     bg=chosen_colors[2], activebackground="#CCE5FF")
send_btn.pack(side=tk.LEFT, padx=5)

mic_btn = tk.Button(entry_frame, text="🎤 Talk", command=lambda: threading.Thread(target=recognize_speech).start(),
                    font=("Comic Sans MS", 12), bg=chosen_colors[2], activebackground="#FFD9E8")
mic_btn.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="", font=("Comic Sans MS", 10), bg=chosen_colors[0], fg="#111")
status_label.pack()

header = tk.Label(root, text="🎉 Hi Bestie! I'm here to listen and chat with you ❤️",
                  font=("Comic Sans MS", 11), bg=chosen_colors[0])
header.pack(pady=5)

footer = tk.Label(root, text="Made by Anushka Sharma with 💖 using Python & GPT",
                  font=("Comic Sans MS", 9), bg=chosen_colors[0], fg="#333")
footer.pack(pady=5)

root.mainloop()
