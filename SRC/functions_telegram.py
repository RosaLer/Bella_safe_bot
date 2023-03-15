from datafunction import api_token, answers, edit_text, token, answers
import telebot

# model
import pickle
import numpy as np
import os

# audio
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

# regex
import re

# Telebot
bot = telebot.TeleBot(api_token.API_TOKEN)

# Open recognicer:
r = sr.Recognizer()

# Open model for the first conversational interaction:
path = 'datafunction'
model = 'interaction_5.pkl'

with open(path+ '/'+ model, "rb") as modelo_2:
    best_model_2 = pickle.load(modelo_2) #pasar por parámetro

def prediction_text(message):
    msg = np.array([token.token_lemma_str(edit_text.clean(message))])
    pred = best_model_2.predict(msg)
    for key, value in answers.respuestas.items():
        if int(pred) == key:
            return value, key

def prediction_int(message):
    msg = np.array([token.token_lemma_str(edit_text.clean(message))])
    pred = best_model_2.predict(msg)
    return int(pred)
        
def voice_to_text(message):
    # capture information from voice message
    voice_info = bot.get_file(message.voice.file_id)
    voice_content = bot.download_file(voice_info.file_path)
    
    # create a temporary file on path:
    with tempfile.NamedTemporaryFile(suffix='.ogg', dir='.') as archivo_temp:
        archivo_temp.write(voice_content)
        archivo_temp.flush()
        archivo_temp.seek(0)
        # change the format to .wav to use speech_recognition
        ogg_audio = AudioSegment.from_ogg(archivo_temp.name)
        wav_audio = tempfile.NamedTemporaryFile(suffix='.wav', dir='.', delete=False)
        wav_audio.close()
        ogg_audio.export(wav_audio.name, format='wav')

        # transcribe received audio
        with sr.AudioFile(wav_audio.name) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='es-ES')
        # delete the file from the path
        os.remove(wav_audio.name)
    # returns the transcript
    return text

def say_hello(message):
    # Detect if incoming message is a greeting or not with regex
    for saludo in answers.saludos:
        patron = re.compile(r'\b{}\b'.format(saludo), re.IGNORECASE)
        if patron.search(edit_text.clean(message)):
            return True
    return False

def say_good_bye(message):
    # Detect if incoming message is goodbye or not with regex
    for despedida in answers.despedidas:
        patron = re.compile(r'\b{}\b'.format(despedida), re.IGNORECASE)
        if patron.search(edit_text.clean(message)):
            return True
    return False
