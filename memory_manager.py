import json
from typing import Tuple

MAX_HISTORY = 5
MAX_CONTEXT_LENGTH = 2000  # batas karakter context, bisa diatur


def load_memory(filename="chat_history.json") -> Tuple[str, list]:
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            context = data.get("context", "Namamu user dan aku Vintec.\n")  # ganti di sini
            history = data.get("history", [])
            if len(history) > MAX_HISTORY:
                history = history[-MAX_HISTORY:]
            return context, history
    except FileNotFoundError:
        return "Namamu user dan aku Vintec.\n", []

def save_memory(context: str, history: list, filename="chat_history.json"):
    # Batasi panjang history sebelum simpan
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    # Ringkas context kalau terlalu panjang (misal potong atau buat summary)
    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[-MAX_CONTEXT_LENGTH:]  # contoh simpel: potong dari belakang

    with open(filename, "w") as file:
        json.dump({"context": context, "history": history}, file, indent=4)
