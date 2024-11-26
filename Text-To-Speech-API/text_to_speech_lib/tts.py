from gtts import gTTS
import io
import base64

def text_to_speech_vietnamese(text):
    tts = gTTS(text=text, lang='vi')
    with io.BytesIO() as audio_file:
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return base64.b64encode(audio_file.read()).decode('utf-8')    

def text_to_speech(text, lang = 'vi'):
    tts = gTTS(text=text, lang=lang)
    with io.BytesIO() as audio_file:
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return base64.b64encode(audio_file.read()).decode('utf-8')

