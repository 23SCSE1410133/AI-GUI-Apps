import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import string
import pyttsx3

# Download NLTK stopwords (only once)
nltk.download('stopwords')

# Sample FAQs
faq_data = [
    {"question": "hello", "answer": "Hi there! How can I help you today?"},
    {"question": "hi", "answer": "Hello! How can I assist you with Artificial Intelligence?"},
    {"question": "hyy", "answer": "Hey! I'm here to answer your questions. Ask me anything!"},
    {"question": "what can you do", "answer": "I'm an AI FAQ chatbot. I can answer questions related to Artificial Intelligence concepts, types, history, and more."},
    {"question": "who are you", "answer": "I'm your friendly FAQ chatbot built to help you understand Artificial Intelligence better."},
    {"question": "thank you", "answer": "You're welcome! Feel free to ask more questions."},
    {"question": "thanks", "answer": "Glad I could help! 😊"},
    {"question": "bye", "answer": "Goodbye! Have a great day. 👋"},
    {"question": "what is artificial intelligence", "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are designed to think and act like humans."},
    {"question": "what are the types of ai", "answer": "AI is generally classified into Narrow AI, General AI, and Super AI based on capability; and Reactive Machines, Limited Memory, Theory of Mind, and Self-Aware AI based on functionality."},
    {"question": "what is machine learning", "answer": "Machine Learning is a subset of AI that enables computers to learn from data and improve over time without being explicitly programmed."},
    {"question": "what is deep learning", "answer": "Deep Learning is a specialized form of Machine Learning that uses deep neural networks to model and solve complex problems like image recognition or speech translation."},
    {"question": "what is the difference between ai and ml", "answer": "AI is the broader concept of machines being able to carry out tasks in a smart way, while ML is a specific application of AI that allows machines to learn from data."},
    {"question": "what are real world applications of ai", "answer": "AI is used in autonomous vehicles, recommendation systems, healthcare diagnosis, fraud detection, virtual assistants, robotics, and many more domains."},
    {"question": "what is computer vision", "answer": "Computer Vision is a field of AI that allows machines to interpret and understand visual information from the world, like images and videos."},
    {"question": "what is natural language processing", "answer": "NLP is a branch of AI focused on enabling computers to understand, interpret, and generate human language."},
    {"question": "what is reinforcement learning", "answer": "Reinforcement Learning is a type of Machine Learning where agents learn to make decisions by receiving rewards or penalties from the environment."},
    {"question": "what is a neural network", "answer": "A neural network is a series of algorithms modeled after the human brain, designed to recognize patterns in data."},
    {"question": "what are the best programming languages for ai", "answer": "Python is the most popular for AI, followed by R, Java, C++, and Julia."},
    {"question": "what are ai frameworks or libraries", "answer": "Popular libraries include TensorFlow, PyTorch, Scikit-learn, Keras, OpenCV, and spaCy."},
    {"question": "how does ai impact jobs", "answer": "AI can replace repetitive jobs, augment complex tasks, and create new career opportunities, but it also raises concerns about job displacement."},
    {"question": "can ai replace humans", "answer": "AI can outperform humans in specific tasks but lacks consciousness, emotional understanding, and ethical reasoning."},
    {"question": "how is ai used in healthcare", "answer": "AI helps in early diagnosis, drug discovery, personalized treatment, robotic surgery, and medical imaging analysis."},
    {"question": "how is ai used in finance", "answer": "AI is used in fraud detection, algorithmic trading, credit risk analysis, customer service chatbots, and personal finance management."},
    {"question": "how is ai used in education", "answer": "AI powers adaptive learning platforms, automated grading, personalized feedback, and virtual tutors."},
    {"question": "how is ai used in e-commerce", "answer": "AI enhances product recommendations, dynamic pricing, inventory management, and customer support."},
    {"question": "what is generative ai", "answer": "Generative AI refers to models that can create new content like text, images, music, or code, such as ChatGPT, DALL·E, and MidJourney."},
    {"question": "what is gpt", "answer": "GPT (Generative Pre-trained Transformer) is a type of large language model developed by OpenAI for generating human-like text."},
    {"question": "what are the risks of ai", "answer": "Risks include biased decisions, job loss, surveillance misuse, deepfakes, lack of accountability, and autonomous weapons."},
    {"question": "what is explainable ai", "answer": "Explainable AI (XAI) refers to AI systems that offer transparency in their decisions, making it easier for humans to understand how outputs were derived."},
    {"question": "what is the turing test", "answer": "The Turing Test is a measure of a machine's ability to exhibit intelligent behavior equivalent to or indistinguishable from that of a human."},
    {"question": "what is the future of ai", "answer": "AI will continue to grow across industries with advancements in general intelligence, responsible AI, and human-AI collaboration."},
    {"question": "what are ethical concerns in ai", "answer": "These include bias, lack of transparency, data privacy violations, misinformation, and the moral responsibility of autonomous systems."},
    {"question": "how do i start learning ai", "answer": "Begin with Python, learn basic math (linear algebra, probability, calculus), study Machine Learning, and practice using libraries like Scikit-learn or TensorFlow."},
    {"question": "what are some good ai courses for beginners", "answer": "Some top beginner courses are 'AI for Everyone' by Andrew Ng, 'Machine Learning' by Stanford on Coursera, and Google's AI training on TensorFlow."},
    {"question": "what is the role of data in ai", "answer": "Data is essential for training AI models. The quality and quantity of data directly impact performance and reliability."},
    {"question": "what is transfer learning in ai", "answer": "Transfer Learning is the process of using a pre-trained model on a new, but related, task to reduce training time and improve results."},
    {"question": "can ai be creative", "answer": "Generative AI models can produce music, art, poetry, and code, but whether this is 'creativity' or imitation is a philosophical debate."},
    {"question": "is ai conscious", "answer": "No, AI lacks consciousness, self-awareness, emotions, and subjective experiences. It processes inputs mathematically."},
    {"question": "can ai be biased", "answer": "Yes, if training data contains biases, the AI may learn and replicate those biases, leading to unfair or discriminatory outcomes."}
]

    

# NLP Preprocessing
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)

# Prepare TF-IDF
processed_questions = [preprocess(faq["question"]) for faq in faq_data]
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)

# Voice Engine Setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass  # Prevents crash if engine is busy


def find_best_match(user_question):
    user_processed = preprocess(user_question)
    if not user_processed.strip():
        return "Please enter a valid question."
    
    user_vector = vectorizer.transform([user_processed])
    similarities = cosine_similarity(user_vector, faq_vectors)
    
    if similarities.max() < 0.2:  # You can tweak this threshold
        return "I'm not sure about that. Try rephrasing your question."
    
    best_idx = similarities.argmax()
    return faq_data[best_idx]["answer"]


# GUI Setup
def send():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    chat_window.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)

    if user_input.lower() in ["exit", "quit", "bye"]:
        response = "Goodbye! Thanks for using the FAQ chatbot."
        chat_window.insert(tk.END, "Bot: " + response + "\n")
        speak(response)
        root.after(1500, root.destroy)
        return

    try:
        response = find_best_match(user_input)
    except:
        response = "Sorry, I didn't understand that."

    chat_window.insert(tk.END, "Bot: " + response + "\n")
    speak(response)
    chat_window.see(tk.END)


# Main Window
root = tk.Tk()
root.title("AI FAQ Bot")
root.geometry("500x550")
root.resizable(False, False)

# Chat history window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=25, font=("Arial", 10))
chat_window.pack(padx=10, pady=10)
chat_window.config(state='normal')
chat_window.insert(tk.END, "🤖 Bot: Hello! Ask me anything from FAQs or type 'exit' to quit.\n")

# Entry field
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5)
entry.bind("<Return>", lambda event: send())
entry.focus()

# Send button
send_button = tk.Button(root, text="Send", command=send, width=10, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
send_button.pack(pady=5)

# Run the app
root.mainloop()
