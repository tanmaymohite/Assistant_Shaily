import pvporcupine
import pyaudio
import struct
import os
from gtts import gTTS
import speech_recognition as sr
import pygame
from datetime import datetime
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import ffmpeg
import numpy as np
import time

# Function to convert text to speech and play it
def speak(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove("response.mp3")

# Function to recognize speech after wake word is detected
def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"User said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Function to handle commands
def handle_command(text):
    if "what is the time right now" in text:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The time is {current_time}."

    elif "identify objects" in text:
        capture_video_and_identify_objects()
    elif "what is my mama name" in text:
        return "Krushnat Khavle."
    elif "what is our favorite song" in text or "what is our favourite song" in text:
        return "Tum Se Hi, by Mohit Chauhan."

    else:
        return "I don't understand the command."

# Function to capture video and identify objects
def capture_video_and_identify_objects():
    # Start capturing video from the camera
    process = (
        ffmpeg
        .input('0')  # Use '0' for default camera
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    while True:
        in_bytes = process.stdout.read(640 * 480 * 3)  # Read 640x480 frames
        if not in_bytes:
            break
        frame = np.frombuffer(in_bytes, np.uint8).reshape([480, 640, 3])

        # Perform object detection or image processing here
        object_name = "Detected Object"  # Replace with actual detection logic

        # Speak the detected object
        speak(f"I see a {object_name}")
        time.sleep(5)  # Wait for 5 seconds

# Create a UI with tkinter
def create_ui():
    window = tk.Tk()
    window.title("Shaily - Your Assistant")
    window.geometry("400x400")

    label = Label(window, text="Assistant Shaily ", font=("Helvetica", 20))
    label.pack(pady=10)

    img = Image.open(r"C:\Users\THOR\Desktop\s\shaily.jpg")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    img_label = Label(window, image=photo)
    img_label.pack(pady=20)

    listening_label = Label(window, text="Listening for 'Shaily'...", font=("Helvetica", 14))
    listening_label.pack(pady=10)

    window.after(100, start_assistant, listening_label)
    window.mainloop()

# Function to start the voice assistant logic
def start_assistant(label):
    porcupine = pvporcupine.create(
        access_key='jmyuGefdLbQzJp6J18wb1MMQ2CBb5rAK9xnAfIGoKWIKUyhnjI7big==',  # Replace with your Picovoice access key
        keyword_paths=[r"C:\Users\THOR\Desktop\project_shaily\hi-shali_en_windows_v3_0_0.ppn"]
    )

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word 'Shaily' detected!")
                label.config(text="Wake word 'Shaily' detected!")
                speak("How can I assist you?")

                command = recognize_speech()
                if command:
                    response = handle_command(command)
                    speak(response)
                label.config(text="Listening for 'Shaily' again...")

    except KeyboardInterrupt:
        print("Stopping the assistant...")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    create_ui()
