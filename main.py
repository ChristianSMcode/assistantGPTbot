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
import json
import os

load_dotenv()

KEYWORD_PATHS   = [os.getenv('KEYWORD_PATH')]
ACCESS_KEY      = os.getenv('ACCESS_KEY_PORCUPINE')
MODEL_PATH      = os.getenv('MODEL_PATH')
LANG_SPEECH     = os.getenv('LANG_SPEECH')
OPENAI_KEY      = os.getenv('OPENAI_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
LANGE_SPEECH_RECOGNITION = os.getenv('LANGE_SPEECH_RECOGNITION')
ENGINE          = os.getenv('ENGINE')
TEMPERATURE     = os.getenv('TEMPERATURE')
MAX_TOKENS      = os.getenv('MAX_TOKENS')
TOP_P           = os.getenv('TOP_P')
FRECUENCY_PENALTY = os.getenv('FRECUENCY_PENALTY')
PRESENCE_PENALTY  = os.getenv('PRESENCE_PENALTY')

openai.api_key = OPENAI_KEY
openai.organization = OPENAI_ORGANIZATION

with open(f'langs-configuration/{LANG_SPEECH.lower()}.json','r') as lang_config:
    data = json.load(lang_config)

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
            audio = r.listen(source)
            text = r.recognize_google(audio,language=LANGE_SPEECH_RECOGNITION)
            return text
        except Exception as e:
            return False
    
def call_gpt(inp,symbol=None,en=ENGINE,temp=TEMPERATURE,max_tokens=MAX_TOKENS,top_p=TOP_P,fp=FRECUENCY_PENALTY,pp=PRESENCE_PENALTY):
    print('inp:', inp)
    response = openai.Completion.create(
        engine=en,
        prompt=inp + symbol,
        temperature=float(temp),
        max_tokens=int(max_tokens),
        top_p=int(top_p),
        frequency_penalty=int(fp),
        presence_penalty=int(pp)
    )
    return response

        
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
            play(generate_audio_data_from_text(data['helloPhrase']))
            while True:
                print('detecting conversation...')
                text = detect_words(r)
                if not text:
                    print('Nothing was detected')
                    break
                response = call_gpt(text,'?')
                play(generate_audio_data_from_text(response['choices'][0]['text']))
                


if __name__ == "__main__":
    main()
    














