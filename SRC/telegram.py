from datafunction import api_token, answers, edit_text, token
import threading
import numpy as np
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telebot import types
import functions_telegram
import time
import re


# Telebot
bot = telebot.TeleBot(api_token.API_TOKEN)

# Vocabulary
vocabulary = edit_text.abrir_text("data/processed_data", "freq_words").split(sep=" ")


# comando ayuda
@bot.message_handler(commands=["ayuda"])
def call_handler(message):
    # envía contactos de emergencia oficiales
    bot.reply_to(message, "Aquí te dejo algunos contactos de emergencia:")
    bot.send_contact(message.chat.id, first_name='Emergencias', phone_number='112')
    time.sleep(1)
    bot.send_contact(message.chat.id, first_name='Policía Nacional', phone_number='091')
    time.sleep(1)
    bot.send_contact(message.chat.id, first_name='Policía local', phone_number='092')
    time.sleep(1)
    bot.send_contact(message.chat.id, first_name='Guardia Civil', phone_number='062')


# responder al comando /start y /hola
@bot.message_handler(commands=["start", "hola"])
def start(message):
    # Da la bienvenida
    bot.reply_to(message, answers.respuestas["Bienvenida"][0])

# responder en caso de saludo
@bot.message_handler(func=lambda message: functions_telegram.say_hello(message.text))
def responder_saludo(message):
    bot.reply_to(message, answers.respuestas["Bienvenida"][0])

# responder en caso de despedida
@bot.message_handler(func=lambda message: functions_telegram.say_good_bye(message.text))
def responder_saludo(message):
    bot.reply_to(message, answers.respuestas["Despedida"][0])


@bot.message_handler(content_types=["text"])
# Gestionar mensajes de texto recibidos
def mensaje_texto(message):
# recibe mensaje, lo limpia, tokeniza y lematiza
# predice qué tipo de respuesta necesita y la devuelve
# si el mensaje trata sobre la temática continúa, si no, devuelve mensaje de error
    msg = token.token_lemma_str(edit_text.clean(message.text))
    if any(palabra in msg.split(" ") for palabra in vocabulary):
        if message.text.startswith("/"):
             bot.send_message(message, "Comando no disponible")
        else:
            # mensaje de "escribiendo"
            bot.send_chat_action(message.chat.id, "typing")
            # predición con el modelo
            pred = functions_telegram.prediction_int(message.text)
            value = functions_telegram.prediction_text(message.text)
            # devuelve respuesta según predicción
            bot.send_message(message.chat.id, value)
            if pred == 0:
                time.sleep(2)
                bot.send_contact(message.chat.id, first_name='Emergencias', phone_number='112')
            elif pred == 2:
                markup = InlineKeyboardMarkup(row_width=3) 
                b1 = InlineKeyboardButton("Policía: Unidad Atención Mujer", url = "https://www.policia.es/_es/colabora_ufam.php")
                b2 = InlineKeyboardButton("Delegación Gov. Violencia Genero", url = "https://violenciagenero.igualdad.gob.es")
                b3 = InlineKeyboardButton("Ayuda psicológica para mujeres", url= "https://www.mujeresparalasalud.org/terapia-psicologica-para-mujeres") 
                markup.add(b1,b2,b3) 
                bot.send_message(message.chat.id, "Información organismos oficiales", reply_markup=markup)
                time.sleep(2)
                bot.send_contact(message.chat.id, first_name='#016 para todas', phone_number='016')
    else:
        bot.reply_to(message, "Lo siento, no he entendido. ¿Podrías repetirlo o intentar decirlo de otra manera?")    
        
# para mensajes de voz
@bot.message_handler(content_types=["voice"])
def mensaje_voice(message):
    
    bot.send_chat_action(message.chat.id, "typing")
    # transcribe el audio 
    text = functions_telegram.voice_to_text(message)
    # lematiza y tokeniza y comprueba que sea un saludo, despedida y de la temática
    msg = token.token_lemma_str(edit_text.clean(text))
    if any(palabra in msg.split(" ") for palabra in answers.saludos):
        bot.reply_to(message, answers.respuestas["Bienvenida"][0])
    elif any(palabra in msg.split(" ") for palabra in answers.despedidas):
        bot.reply_to(message, answers.respuestas["Despedida"][0])
    elif any(palabra in msg.split(" ") for palabra in vocabulary):
        # predición con el modelo
        pred = functions_telegram.prediction_int(msg)
        value = functions_telegram.prediction_text(msg)
        # devuelve respuesta según predicción
        bot.send_message(message.chat.id , value)
        if pred == 0:
                time.sleep(2)
                bot.send_contact(message.chat.id, first_name='Emergencias', phone_number='112')
        elif pred == 2:
                markup = InlineKeyboardMarkup(row_width=3) 
                b1 = InlineKeyboardButton("Policía: Unidad Atención Mujer", url = "https://www.policia.es/_es/colabora_ufam.php")
                b2 = InlineKeyboardButton("Delegación Gov. Violencia Genero", url = "https://violenciagenero.igualdad.gob.es")
                b3 = InlineKeyboardButton("Ayuda psicológica para mujeres", url= "https://www.mujeresparalasalud.org/terapia-psicologica-para-mujeres") 
                markup.add(b1,b2,b3) 
                bot.send_message(message.chat.id, "Información organismos oficiales", reply_markup=markup)
                time.sleep(2)
                bot.send_contact(message.chat.id, first_name='#016 para todas', phone_number='016')
    
    else: 
        bot.reply_to(message, "Lo siento, no he entendido. ¿Podrías repetirlo o intentar decirlo de otra manera?")



def recibir_mensajes():
    #Bucle infinito que espera siempre recibir mensajes
    bot.infinity_polling()


# MAIN ########################
if __name__ == '__main__':
    # Comandos de emergencia:
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Bienvenida"),
        telebot.types.BotCommand("/ayuda", "Contactos de emergencia")
    ])
    print("Iniciando el bot")
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print("Bot iniciado")