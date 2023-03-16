import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv
import openai
import os

load_dotenv()

KEYWORD_PATHS   = [os.getenv('KEYWORD_PATH')]
ACCESS_KEY      = os.getenv('ACCESS_KEY_PORCUPINE')
MODEL_PATH      = os.getenv('MODEL_PATH')
LANG_SPEECH     = os.getenv('LANG_SPEECH')

def instanciate_classes():
    porcupine = pvporcupine.create(keyword_paths=KEYWORD_PATHS, access_key=ACCESS_KEY, model_path=MODEL_PATH)
    p = pyaudio.PyAudio()
    r = sr.Recognizer()
    return [porcupine, p, r]

def detect_hotword(stream,porcupine):
    pcm = stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length,pcm)
    keyword_index = porcupine.process(pcm)
    return keyword_index

def generate_audio_data_from_text(text):
    audio_file = BytesIO()
    tts = gTTS(text,lang=LANG_SPEECH)
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    audio_data= AudioSegment.from_file(audio_file,format='mp3')
    return audio_data

def detect_words(r):
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            return False
    
def call_gpt(input):
    pass

        
def main():
    porcupine,p,r = instanciate_classes()
    
    FORMAT   = pyaudio.paInt16 
    CHANNELS = 1
    RATE     = porcupine.sample_rate
    CHUNK    = porcupine.frame_length

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, input=True)

    while True:
        keyword_index = detect_hotword(stream,porcupine)
        if keyword_index >= 0:
            play(generate_audio_data_from_text('Hola en que puedo ayudarte'))
            while True:
                text = detect_words(r)
                if not text:
                    print('Nothing was detected')
                    break
                response = call_gpt(text)
                play(generate_audio_data_from_text(response))
                


if __name__ == "__main__":
    main()
    














