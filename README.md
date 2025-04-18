🤖 Shaily - Your Personal Voice Assistant

**Shaily** is a voice assistant that uses wake word detection, speech recognition, and local LLM (Gemma 3B via Ollama) to give intelligent and personal responses.

---

## 🌟 Features

- 🎙️ Wake word detection using **Picovoice Porcupine**
- 🗣️ Speech recognition using **SpeechRecognition (Google API)**
- 🧠 Smart replies generated using **Gemma 3B model** via **Ollama**
- 🔊 Text-to-speech using **gTTS** and playback via **pygame**
- 🖥️ Simple GUI made with **Tkinter**

---

## 🔧 Setup Instructions (Run Locally on Any Laptop)

### 1. Clone this Repository
```bash
git clone https://github.com/your-username/shaily-assistant.git
cd shaily-assistant
```

### 2. Install Python
Ensure you have **Python 3.10+** installed. You can download from [python.org](https://www.python.org/).

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Install and Run Ollama
- Download and install [Ollama](https://ollama.com/)
- Run the Gemma model:
```bash
ollama run gemma3:1b
```

### 6. Download Wake Word (.ppn file)
- Sign up at [Picovoice Console](https://console.picovoice.ai/)
- Create a custom keyword (e.g., “Shaily” or “Shelly”)
- Download and extract the `.ppn` file
- Place it in your project directory

### 7. Add Your Picovoice Access Key
Replace `'YOUR_ACCESS_KEY'` in the code with your actual key from Picovoice.

### 8. Run the Assistant
```bash
python main.py
```

---

## 🤖 How It Works
1. Listens for the wake word (e.g., “Shaily”)
2. Activates microphone and records user input
3. Sends the text to **Gemma 3B model** via **Ollama API**
4. Converts the response to speech
5. Speaks the response back to the user

---

## 💡 Why the Name "Shaily"?
The name "Shaily" holds a special significance. It was inspired by a girl I met during a Garba event. She was beautiful, kind, unique, and perfect. Her name was equally unique—there's hardly any name like it in India. I thought it would be the perfect name for my project, symbolizing individuality and excellence.

---

## 📂 Folder Structure
```
shaily-assistant/
├── main.py              # Main script with wake word + speech + UI
├── requirements.txt     # Required Python packages
├── README.md            # You're here!
├── hey-shelly.ppn       # Wake word model file (download separately)
└── ...
```

---

## 🙌 Credits
- [Picovoice](https://picovoice.ai/)
- [Ollama](https://ollama.com/)
- [gTTS](https://pypi.org/project/gTTS/)
- [pygame](https://www.pygame.org/)
- [Python SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

---

## 📬 Future Plans
- Add memory/chat history
- Use custom voice or real-time TTS engine
- GUI enhancements with buttons & animations
- Packaging into a proper desktop app with installer

---

## 💌 Contributing
Pull requests are welcome! Feel free to open issues or suggest features.

---

## 🔒 Disclaimer
All responses are generated by a local LLM. No data is sent to cloud servers.

---

## 👤 Developer
**Tanmay Mohite**  
_Assisted by ChatGPT_

---
