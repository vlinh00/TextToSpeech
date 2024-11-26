from gtts import gTTS
import os
import base64

def text_to_speech_vietnamese(text, filename='output.mp3'):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)

    with open(filename, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    return encoded_string

def text_to_speech(text, lang='vi', filename='output.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    with open(filename, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    return encoded_string
