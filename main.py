import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv
import os

load_dotenv()

KEYWORD_PATHS = [os.getenv('KEYWORD_PATH')]
ACCESS_KEY=os.getenv('ACCESS_KEY_PORCUPINE')
MODEL_PATH=os.getenv('MODEL_PATH')

def instanciate_classes():
    porcupine = pvporcupine.create(keyword_paths=KEYWORD_PATHS, access_key=ACCESS_KEY, model_path=MODEL_PATH)
    p = pyaudio.PyAudio()
    return [porcupine, p]

def detect_hotword(stream,porcupine):
    pcm = stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length,pcm)
    keyword_index = porcupine.process(pcm)
    return keyword_index

def main():
    porcupine,p = instanciate_classes()
    
    FORMAT   = pyaudio.paInt16 
    CHANNELS = 1
    RATE     = porcupine.sample_rate
    CHUNK    = porcupine.frame_length

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, input=True)

    while True:
        keyword_index = detect_hotword(stream,porcupine)
        if keyword_index >= 0:
            print('HOT WORD DETECTED')
    
if __name__ == "__main__":
    main()
    














