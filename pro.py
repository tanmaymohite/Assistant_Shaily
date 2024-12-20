import pvporcupine
import pyaudio
import struct
import os
from gtts import gTTS
import speech_recognition as sr
import pygame
from datetime import datetime  # Import datetime for time functionality
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk  # For handling images in tkinter


# Function to convert text to speech and play it
def speak(response):
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")  # Load the MP3 file
    pygame.mixer.music.play()  # Play the MP3 file

    # Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Sleep to allow audio to play

    # Stop and unload the music to release the file
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    # Now delete the file after it's fully released
    os.remove("response.mp3")


# Function to play favorite song
def play_favorite_song(song_path):
    # Initialize pygame mixer if it's not initialized yet
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Load the song and play it
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    # Wait for the song to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Allow the music to play smoothly


# Function to recognize speech after wake word is detected
def recognize_speech():
    recognizer = sr.Recognizer()

    # Try increasing sensitivity by lowering pause threshold and setting dynamic energy
    recognizer.pause_threshold = 1.0  # Adjusting pause time (default is 0.8)
    recognizer.dynamic_energy_threshold = True  # Dynamically adjusts the energy threshold

    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adapts to ambient noise in the room
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
def handle_command(text, song_path):
    if "what is the time right now" in text:
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")  # Format as 12-hour clock with AM/PM
        return f"The time is {current_time}."
    elif "what is weather right now" in text:
        return "The weather is sunny."
    elif "what are you doing" in text:
        return "Just completing my assingments , they are so much."
    elif "what is our favorite song" in text or "what is our favourite song" in text:
        return "Tum Se Hi, by Mohit Chauhan."
    elif "play my favourite song" in text:
        speak("Playing your favorite song now.")
        play_favorite_song(song_path)  # Play the favorite song
        return "Playing your favorite song."
    elif "suggest me a new smartphone" in text:
        return "Samsung Galaxy S23 Ultra."
    elif "what is my father name" in text:
        return "Rajendra Mohite."
    elif "what is my mum name" in text:
        return "Rajashri Mohite."
    elif "what is my pin number" in text:
        return "2103069."
    elif "what is my mama name" in text:
        return "Krushnat Khavle."
    elif "what do you love doing" in text:
        return "I like to play Garba."
    elif "in which college you are studying" in text:
        return "PCCOE R."
    elif "you are so cute" in text:
        return "Padhai pe dhyan de."
    elif "where are you from" in text:
        return "I am from Gujarat."
    elif "when did we meet first time" in text:
        return "In Ganesh Talav while playing Garba."
    elif "when are you going to send me my photos" in text:
        return "I will send you soon."
    elif "do you wear chashma" in text:
        return "Yes, I do wear chashma."
    elif "thank you so much" in text:
        return "You're always welcome, Tanmay."

    else:
        return "I don't understand the command."


# Create a UI with tkinter
def create_ui(song_path):
    # Create the main window
    window = tk.Tk()
    window.title("Shaily - Your Assistant")
    window.geometry("400x400")

    # Add a label to display a title
    label = Label(window, text="Assistant Shaily ", font=("Helvetica", 20))
    label.pack(pady=10)

    # Load an image and display it in the window
    img = Image.open(r"C:\Users\THOR\Desktop\project_shaily\shaily_image.jpg" )  # Replace with the correct path to your image file
    img = img.resize((200, 200), Image.Resampling.LANCZOS)  # Resize image using LANCZOS instead of ANTIALIAS
    photo = ImageTk.PhotoImage(img)
    img_label = Label(window, image=photo)
    img_label.pack(pady=20)

    # Add a label to indicate the assistant is listening
    listening_label = Label(window, text="Listening for 'Shaily'...", font=("Helvetica", 14))
    listening_label.pack(pady=10)

    # Call the blink function for blinking effect
    blink_label(listening_label)

    # Start the tkinter main loop
    window.after(100, start_assistant, listening_label, song_path)  # Start the assistant after UI loads
    window.mainloop()


# Function to blink the 'Listening for Shaily...' label
def blink_label(label):
    current_color = label.cget("fg")
    next_color = "green" if current_color == "black" else "black"
    label.config(fg=next_color)

    # Repeat the function after 500 milliseconds
    label.after(500, blink_label, label)


# Function to start the voice assistant logic
def start_assistant(label, song_path):
    # Initialize Porcupine with access key and wake word path
    porcupine = pvporcupine.create(
        access_key='jmyuGefdLbQzJp6J18wb1MMQ2CBb5rAK9xnAfIGoKWIKUyhnjI7big==',  # Replace with your Picovoice access key
        keyword_paths=[r"C:\Users\THOR\Desktop\project_shaily\hi-shali_en_windows_v3_0_0.ppn"]
        # Correct path to your downloaded wake word .ppn file
    )

    pa = pyaudio.PyAudio()

    # Audio stream configuration
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

            # Detect wake word
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word 'Shaily' detected!")
                label.config(text="Wake word 'Shaily' detected!")
                speak("How can I assist you?")

                # Capture the actual command after wake word is detected
                command = recognize_speech()

                if command:
                    response = handle_command(command, song_path)
                    speak(response)

                # After executing the command, continue listening for the next command
                print("Listening for 'Shaily' again...")
                label.config(text="Listening for 'Shaily' again...")

    except KeyboardInterrupt:
        print("Stopping the assistant...")
    finally:
        # Cleanup resources
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    # Provide the path to the favorite song here
    favorite_song_path = r"C:\Users\THOR\Downloads\Tum_Se_Hi_(Jab_We_Met)_320_Kbps.mp3"
    create_ui(favorite_song_path)
