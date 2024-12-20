import pvporcupine
import pyaudio
import struct
import os
from gtts import gTTS
import speech_recognition as sr
import pygame


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
def handle_command(text):
    if "what is weather rightnow" in text:
        return "The weather is sunny."
    elif "what are you doing" in text:
        return "just thinking about you"
    elif "what is our favorite song" in text:
        return "tum se he ,by mohit chuhan"
    elif "what is our favourite song" in text:
        return "tum se he ,by mohit chuhan"
    elif "suggest me a new smartphone" in text:
        return "samsung galaxy s23 ultra"
    elif "suggest me a new smartphone" in text:
        return "samsung galaxy s23 ultra"
    elif "what is my father name" in text:
        return "rajendra mohite"
    elif "what is my mum name" in text:
        return "rajashri mohite"
    elif "what is my pin number" in text:
        return "2103069"
    elif "what is my mama name" in text:
        return "krushnat khavle"
    elif "what do you love doing" in text:
        return "i like to play garba"
    elif "in which college you are studying" in text:
        return "pccoe r"
    elif "you are so cute" in text:
        return "padhai pe dhyan de bhos di ke"
    elif "where are you from" in text:
        return "Iam from gujarat"
    elif "when did we meet first time" in text:
        return "in ganesh talav while playing garba"
    elif "when you are going to send me my photos" in text:
        return "i will send you soon"
    elif "do you wear chashma" in text:
        return "yes i do wear chashma"
    elif "thank you so much" in text:
        return "your always welcome tanmay"
    else:
        return "I don't understand the command."


if __name__ == "__main__":
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

    print("Listening for 'Shaily'...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Detect wake word
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word 'Shaily' detected!")
                speak("How can I assist you?")

                # Capture the actual command after wake word is detected
                command = recognize_speech()

                if command:
                    response = handle_command(command)
                    speak(response)

                # After executing the command, continue listening for the next command
                print("Listening for 'Shaily' again...")

    except KeyboardInterrupt:
        print("Stopping the assistant...")
    finally:
        # Cleanup resources
        audio_stream.close()
        pa.terminate()
        porcupine.delete()
