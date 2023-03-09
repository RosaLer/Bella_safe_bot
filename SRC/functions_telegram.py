from datafunction import api_token, answers, edit_text, token, answers
import telebot

# modelo
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

# Se abre recognicer:
r = sr.Recognizer()

# Carga modelo primera interacción:
with open('datafunction/interaction_5.pkl', "rb") as modelo_2:
    best_model_2 = pickle.load(modelo_2)

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
    # captura la información del mensaje de voz 
    voice_info = bot.get_file(message.voice.file_id)
    voice_content = bot.download_file(voice_info.file_path)
    
    # crea un archivo temporal en el path:
    with tempfile.NamedTemporaryFile(suffix='.ogg', dir='.') as archivo_temp:
        archivo_temp.write(voice_content)
        archivo_temp.flush()
        archivo_temp.seek(0)
        # cambio de formato a .wav para pasarlo a speech_recognition
        ogg_audio = AudioSegment.from_ogg(archivo_temp.name)
        wav_audio = tempfile.NamedTemporaryFile(suffix='.wav', dir='.', delete=False)
        wav_audio.close()
        ogg_audio.export(wav_audio.name, format='wav')

        # transcribe el audio recibido
        with sr.AudioFile(wav_audio.name) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='es-ES')
        # elimina el archivo del path
        os.remove(wav_audio.name)
    # devuelve la transcripción
    return text

def say_hello(message):
    # Detecta si el mensaje entrante es un saludo o no con expresiones regulares
    for saludo in answers.saludos:
        patron = re.compile(r'\b{}\b'.format(saludo), re.IGNORECASE)
        if patron.search(edit_text.clean(message)):
            return True
    return False

def say_good_bye(message):
    # Detecta si el mensaje entrante es una despedida o no con expresiones regulares
    for despedida in answers.despedidas:
        patron = re.compile(r'\b{}\b'.format(despedida), re.IGNORECASE)
        if patron.search(edit_text.clean(message)):
            return True
    return False
