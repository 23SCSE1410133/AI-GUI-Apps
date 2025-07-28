import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pyperclip
import os
from playsound import playsound

# Initialize translator
translator = Translator()

# Setup GUI window
root = tk.Tk()
root.title("Language Translator")
root.geometry("700x400")
root.resizable(False, False)

# Function to translate text
def translate_text():
    try:
        src = source_lang.get()
        dest = target_lang.get()
        input_text = source_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        translated = translator.translate(
            text=input_text,
            src=lang_codes[src],
            dest=lang_codes[dest]
        )
        translated_text.delete("1.0", tk.END)
        translated_text.insert(tk.END, translated.text)

    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# Function to copy translated text
def copy_text():
    output = translated_text.get("1.0", tk.END).strip()
    if output:
        pyperclip.copy(output)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

# Function to speak translated text
def speak_text():
    output = translated_text.get("1.0", tk.END).strip()
    if output:
        lang = lang_codes[target_lang.get()]
        try:
            tts = gTTS(text=output, lang=lang)
            tts.save("temp.mp3")
            playsound("temp.mp3")
            os.remove("temp.mp3")
        except Exception as e:
            messagebox.showerror("TTS Error", f"Failed to speak:\n{str(e)}")

# GUI Layout
tk.Label(root, text="Enter Text", font=("Arial", 12)).place(x=100, y=20)
tk.Label(root, text="Translated Text", font=("Arial", 12)).place(x=450, y=20)

source_text = tk.Text(root, height=10, width=30, font=("Arial", 12))
source_text.place(x=30, y=50)

translated_text = tk.Text(root, height=10, width=30, font=("Arial", 12))
translated_text.place(x=370, y=50)

# Dropdowns for languages
lang_codes = {name.title(): code for code, name in LANGUAGES.items()}
language_list = sorted(lang_codes.keys())

source_lang = ttk.Combobox(root, values=language_list, width=25)
source_lang.place(x=100, y=250)
source_lang.set("English")

target_lang = ttk.Combobox(root, values=language_list, width=25)
target_lang.place(x=450, y=250)
target_lang.set("Hindi")

# Buttons
tk.Button(root, text="Translate", command=translate_text, bg="blue", fg="white", width=15).place(x=300, y=200)
tk.Button(root, text="Copy", command=copy_text, width=10).place(x=370, y=300)
tk.Button(root, text="Speak", command=speak_text, width=10).place(x=470, y=300)

root.mainloop()
