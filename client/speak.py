from openai import OpenAI
import os
from dotenv import load_dotenv
import time
from pygame import mixer

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def speak(message):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=message,
    )

    # Access the audio content directly
    with open("output.mp3", "wb") as f:
        f.write(response.content)

    mixer.init()
    mixer.music.load("output.mp3")
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)

# speak("I think that multithreading is best explained with an example.")