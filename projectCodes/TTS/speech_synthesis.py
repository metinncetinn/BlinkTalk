from gtts import gTTS
import os

def text_to_speech(text):
    tts = gTTS(text=text, lang='tr')
    filename = "speech.mp3"
    tts.save(filename)
    os.system(f"start {filename}")

#text_to_speech("Merhaba.")