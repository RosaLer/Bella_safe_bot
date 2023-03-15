import os
import re

import nltk
from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords.words('spanish')
stop_en = stopwords.words('english')

# visualización
from collections import defaultdict
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as py


# Función para abrir los textos y los devuelve

def abrir_text(carpeta, titulo):
    ruta = carpeta + "/" + titulo + ".txt"
    with open(ruta, "r",  encoding='utf-8') as archivo:
        texto = archivo.read()
    return texto

# Funciones para la limpieza del texto:

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\“)|(\”)|(\')|(\»)|(\«)|(\()|(\))|(\[)|(\])|(\d+)|(\¿)|(\¡)|(\%)")
REPLACE_WITH_SPACE = re.compile("(<br \s*/><br\s*/>)|(\-)|(\/)") 
NO_SPACE = ""
SPACE = " "

def clean(texto):
    dato = REPLACE_NO_SPACE.sub(NO_SPACE, texto.lower())
    dato = REPLACE_WITH_SPACE.sub(SPACE, dato)
    dato = " ".join([word for word in dato.split() if "http" not in word])
    
    return dato

# Function to extract the text of the tags and clean it using the previously generated function:

def extraer_limpiar(tags):
    texto = ""
    for tag in tags:
        texto += tag.text
    limpio_texto = clean(texto)
    
    return limpio_texto

def sum_relevant_words(df, relevant_words, target):
    for col in df.columns:
        if col in relevant_words:
            targ = df["target_2"]==target
            df.loc[targ, col]+= 0.2
            
    return df

# generate ngram: 
def generate_ngrams(text, n_gram=1):
    token = [token for token in text.lower().split(" ") if token != "" if token not in STOPWORDS]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    return [" ".join(ngram) for ngram in ngrams]

# horizontal bar:
def horizontal_bar_chart(df, color):
    trace = go.Bar(
        y=df["word"].values[::-1],
        x=df["wordcount"].values[::-1],
        showlegend=False,
        orientation = 'h',
        marker=dict(
            color=color,
        ),
    )
    return trace
