# AI Ingatan

AI Ingatan (AI Memory) is an interactive chat application with memory capabilities, powered by a local Large Language Model (LLM). The application allows users to interact with an AI assistant named Vintec through both text and voice interfaces in Indonesian language.

## Features

- **Dual Input Modes**: Choose between text or voice input
- **Dual Output Modes**: Choose between text or voice output
- **Memory Functionality**: The AI remembers information about the user across sessions
- **Voice Recognition**: Uses Google's Speech Recognition API to convert speech to text
- **Text-to-Speech**: Converts AI responses to spoken audio using gTTS
- **Local LLM Integration**: Connects to a local LM Studio instance for AI responses

## Requirements

- Python 3.8+
- LM Studio running locally on port 1234
- Microphone (for voice input)
- Speakers (for voice output)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-ingatan.git
   cd ai-ingatan
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Make sure LM Studio is installed and running locally with the API server enabled on port 1234.

## Usage

1. Start the application:
   ```
   python chat_main.py
   ```

2. Enter your name when prompted.

3. Choose your preferred input method (text or voice) by entering 1 or 2.

4. Choose your preferred output method (text or voice) by entering 1 or 2.

5. Start chatting with Vintec!

### Special Commands

- Type "exit" or "selesai" to end the conversation
- Say "tolong ingat [information]" to have the AI remember specific information
- Ask "nama aku siapa" to have the AI recall your name

## Project Structure

- `chat_main.py`: Main application entry point
- `ai_llm.py`: LLM integration with LM Studio
- `memory_manager.py`: Handles saving and loading conversation context and history
- `chat_history.json`: Stores conversation data between sessions
- `tests/`: Contains test files for the application

## Testing

Run the tests using pytest:
```
pytest
```

## Dependencies

- langchain_core: For LLM integration
- pydantic: For data validation
- requests: For API communication
- SpeechRecognition: For voice input
- gTTS: For text-to-speech conversion
- pygame: For audio playback
- pytest: For testing

## 🤝 Contributing

Got ideas or fixes? Let's build together! ✨

```bash
git checkout -b feature/your-feature
git commit -m "Add something awesome"
git push origin feature/your-feature
```

## 📲 Connect with Me

Stay in touch & let's collab! 👇  
- 🐦 [Twitter](https://X.com/swagtutupkup)  
- 💻 [GitHub](https://github.com/vincensiuselang)  
- 📸 [Instagram](https://www.instagram.com/vincenelang)  
- 🎵 [Tiktok](https://www.tiktok.com/@vintec69.pkl)

---

> _Made with coffee ☕, curiosity 🧠, and some real late nights 🌙 by Vincen_
