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

print(f"🤖 Selamat datang di AI Ingatan 🤖\n")

# Minta input nama user sekali di awal program
user_name = input("Halo! Siapa namamu : ").strip()
if not user_name:
    user_name = "Teman"  # fallback

# Set context awal dan kosongkan history
context = f"Namamu {user_name} dan aku Vintec.\n"
history = []

# Simpan ke file di awal
save_memory(context, history)

# Buat folder suara jika belum ada
if not os.path.exists("suara"):
    os.makedirs("suara")

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Ngomong sekarang (tunggu AI jawab)...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="id-ID")
        print(f"kamu (via suara): {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Suara tidak dikenali.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Gagal menghubungi API Google: {e}")
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
        print(f"Warning: gagal hapus file {filepath}")

input_mode = input("Mau input via (1) Teks atau (2) Suara? [1/2]: ")
output_mode = input("Mau output AI dalam bentuk (1) Teks atau (2) Suara? [1/2]: ")

while True:
    if input_mode == "2":
        user_input = get_voice_input()
    else:
        user_input = input("kamu: ")

    # Khusus buat jawab pertanyaan "nama aku siapa?"
    if user_input.lower() in ["nama aku siapa", "siapa nama aku"]:
        response = f"Nama kamu adalah {user_name}."
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
        print("Percakapan Selesai.")
        delete_all = input("Mau hapus semua file audio sementara? [y/n]: ").lower()
        if delete_all == 'y':
            for file in os.listdir("suara"):
                if file.endswith(".mp3"):
                    try:
                        os.remove(os.path.join("suara", file))
                    except Exception as e:
                        print(f"❌ Gagal hapus {file}: {e}")
        break

print("Terima kasih telah menggunakan program ini!")
