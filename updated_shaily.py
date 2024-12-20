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
import cv2
import numpy as np

# Load the classes for object detection
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
           "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
           "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Load pre-trained MobileNet model
net = cv2.dnn.readNetFromCaffe(
    r"C:\Users\THOR\Desktop\project_shaily\opencv\deploy.prototxt",  # Path to prototxt
    r"C:\Users\THOR\Desktop\project_shaily\opencv\mobilenet_iter_73000.caffemodel"  # Path to caffemodel
)


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


# Function to capture video and identify objects
def capture_video_and_identify_objects():
    cap = cv2.VideoCapture(0)

    # Create a new window using Tkinter for video feed
    window = tk.Toplevel()
    window.title("Object Detection")
    label = tk.Label(window)
    label.pack()

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            window.after(10, update_frame)
            return

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                label_text = CLASSES[idx]

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label_text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert frame to RGB (Tkinter uses PIL for image handling)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        window.after(10, update_frame)

    update_frame()
    window.mainloop()

    cap.release()


# Function to handle commands
def handle_command(text):
    if "what is the time right now" in text:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The time is {current_time}."
    elif "identify objects" in text:
        capture_video_and_identify_objects()
        return "Identifying objects..."
    elif "play my favorite song" in text:
        # Replace this with your actual song path
        song_path = r"C:\Users\THOR\Desktop\project_shaily\favorite_song.mp3"
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        return "Playing your favorite song."
    else:
        return "I don't understand the command."


# Create a UI with tkinter
def create_ui():
    window = tk.Tk()
    window.title("Shaily - Your Assistant")
    window.geometry("400x400")

    label = Label(window, text="Assistant Shaily", font=("Helvetica", 20))
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
        access_key='jmyuGefdLbQzJp6J18wb1MMQ2CBb5rAK9xnAfIGoKWIKUyhnjI7big==',
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
