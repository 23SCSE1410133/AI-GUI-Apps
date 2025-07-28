import g4f
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # female voice

# You MUST give a valid model. Let's use gpt-4 or gpt-3.5 supported by g4f
def chat_with_gpt(prompt):
    response = g4f.ChatCompletion.create(
        model='gpt-4',  # ✅ Can also try 'gpt-3.5-turbo' if supported again
        messages=[{"role": "user", "content": prompt}]
    )
    return response

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("🤖 Chatbot: Hello! Ask me anything. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Chatbot: Goodbye! 👋")
            speak("Goodbye!")
            break
        try:
            reply = chat_with_gpt(user_input)
            print("🤖 Chatbot:", reply)
            speak(reply)
        except Exception as e:
            print("⚠️ Chatbot Error:", e)
            speak("Sorry, something went wrong.")
