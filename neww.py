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

import requests

def handle_command(text):
    try:
        prompt = f"{text} Provide a concise answer in 1-2 sentences."
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "gemma3:1b",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "I'm not sure how to respond to that.")
        else:
            return "Sorry, I'm having trouble connecting to my brain (Gemma)."
    except Exception as e:
        return f"Error: {str(e)}"


def create_ui():
    window = tk.Tk()
    window.title("Shaily - Your Assistant")
    window.geometry("400x200")
    label = Label(window, text="Assistant Shaily", font=("Helvetica", 20))
    label.pack(pady=20)
    listening_label = Label(window, text="Listening for 'Shaily'...", font=("Helvetica", 14))
    listening_label.pack(pady=10)
    blink_label(listening_label)
    window.after(100, start_assistant, listening_label)
    window.mainloop()


def blink_label(label):
    current_color = label.cget("fg")
    next_color = "green" if current_color == "black" else "black"
    label.config(fg=next_color)
    label.after(500, blink_label, label)


def start_assistant(label):
    porcupine = pvporcupine.create(
        access_key='Q1lSZkMVeYvdw9C84Bgt2CqO/RgdYR3aNh1ug93LoaS2tv5WIWmRFA==',
        keyword_paths=[r"C:\Users\TANMAY\OneDrive\Desktop\llm\hey-shelly_en_windows_v3_0_0.ppn"]
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
                print("Listening for 'Shaily' again...")
                label.config(text="Listening for 'Shaily' again...")

    except KeyboardInterrupt:
        print("Stopping the assistant...")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    create_ui()
