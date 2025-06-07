# chat_main.py

import speech_recognition as sr
from ai_llm import LMStudioLLM
from memory_manager import load_memory, save_memory
from gtts import gTTS
import os
import uuid
import pygame
import time

llm = LMStudioLLM()

print(f"🤖 Welcome to AI Memory 🤖\n")

# Minta input nama user sekali di awal program
user_name = input("Halo! What is your name : ").strip()
if not user_name:
    user_name = "Brother"  # fallback

# Set context awal dan kosongkan history
context = f"Your name is {user_name} and I'm Vintec.\n"
history = []

# Simpan ke file di awal
save_memory(context, history)

# Buat folder suara jika belum ada
if not os.path.exists("suara"):
    os.makedirs("suara")

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 By the way now (wait for AI to answer)...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="id-ID")
        print(f"You (via voice): {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Voice not recognized.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Failed to contact Google API: {e}")
        return ""

def speak(text):
    tts = gTTS(text=text, lang='id')
    filename = f"temp_{uuid.uuid4()}.mp3"
    filepath = os.path.join("suara", filename)
    tts.save(filepath)

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    time.sleep(0.3)
    pygame.mixer.quit()

    for _ in range(5):
        try:
            os.remove(filepath)
            break
        except PermissionError:
            time.sleep(0.5)
    else:
        print(f"Warning: failed to delete file {filepath}")

input_mode = input("Do you want to input via (1) Text or (2) Voice? [1/2]: ")
output_mode = input("Do you want AI output in the form of (1) Text or (2) Voice? [1/2]: ")

while True:
    if input_mode == "2":
        user_input = get_voice_input()
    else:
        user_input = input("You: ")

    # Khusus buat jawab pertanyaan "nama aku siapa?"
    if user_input.lower() in ["what is my name", "what's my name"]:
        response = f"Your name is {user_name}."
        print(f"AI: {response}")
        if output_mode == "2":
            speak(response)
        continue

    # Kalau user minta ingat sesuatu
    if "tolong ingat" in user_input.lower():
        context += f"Kamu minta untuk ingat: {user_input}.\n"
        if "nama aku" in user_input.lower():
            parts = user_input.lower().split("nama aku", 1)[1].strip().split()
            if parts:
                user_name = parts[0]
                context = f"Namamu {user_name} dan aku Vintec.\n"
                print(f"AI: Baik, aku akan mengingat nama kamu, {user_name}.")
                save_memory(context, history)
                continue

    # Prompt ke LLM
    prompt = context + "\n".join(
        [f"### {user_name}: {msg['user']}\n### Vintec: {msg['Vintec']}" for msg in history]
    ) + f"\n### {user_name}: {user_input}\n### Vintec:"

    ai_response = llm.invoke(prompt)
    print(f"AI: {ai_response}")

    if output_mode == "2":
        speak(ai_response)

    history.append({"user": user_input, "Vintec": ai_response})
    if len(history) > 5:
        history = history[-5:]

    save_memory(context, history)

    if user_input.lower() in ["exit", "selesai"]:
        print("Conversation Completed.")
        delete_all = input("Want to delete all temporary audio files? [y/n]: ").lower()
        if delete_all == 'y':
            for file in os.listdir("suara"):
                if file.endswith(".mp3"):
                    try:
                        os.remove(os.path.join("suara", file))
                    except Exception as e:
                        print(f"❌ Delete failure {file}: {e}")
        break

print("Thank you for using this program!")
