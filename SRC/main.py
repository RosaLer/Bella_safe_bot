from datafunction import api_token, edit_text, extraer, token
import os
import numpy as np
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pickle

# Importar DF con todos los textos:

df_all = pd.read_csv("data/processed_data/all_text.csv")

# Importar DF con palabras elegidas para variar sus pesos:

choos_words = pd.read_excel("data/processed_data/freq_words.xlsx", sheet_name="choos_words")

# Token y lemmatización por texto:

df_all["token_lemma_lst"] = [token.token_lemma_list(row) for row in df_all["textos"]]
df_all["token_lemma_str"] = [token.token_lemma_str(row) for row in df_all["textos"]]

target_2 = [1,1,1,1,1,2,2,1,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,1,1,1]
df_all["target_2"] = target_2

# Aumento del peso de ciertas palabras en ciertas categorías en las que aparecen:

texto = df_all["token_lemma_str"]
target = df_all["target_2"]

def ajust(X,y,choos_words):
# Nuevo vectorizador de TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_trans = tfidf_vectorizer.fit_transform(X)
    
    relevant_words_0 = np.array(choos_words[choos_words["categoría"]==0]["palabras"])
    relevant_words_1 = np.array(choos_words[choos_words["categoría"]==1]["palabras"])
    relevant_words_2 = np.array(choos_words[choos_words["categoría"]==2]["palabras"])
    df_pon = pd.DataFrame(tfidf_trans.toarray(), 
                           columns = tfidf_vectorizer.get_feature_names_out())
    df_pon_tar = pd.concat([df_pon, y], axis=1)
    df_pon_0 = edit_text.sum_relevant_words(df_pon_tar, relevant_words_0, 0)
    df_pon_1 = edit_text.sum_relevant_words(df_pon_0, relevant_words_1, 1)
    df_pon_2 = edit_text.sum_relevant_words(df_pon_1, relevant_words_2, 2)
    
    return df_pon_2, tfidf_vectorizer

df_pon, tf_vec = ajust(texto,target,choos_words)

# Definir X,y:

X = df_pon.iloc[:,:-1]
y = df_pon["target_2"]

model =  LogisticRegression()

# Aqui definimos el espacio de parámetros a explorar
parameters = {
    'C': (0.2, 0.5, 0.7),
    'penalty': (None, "l2"),
    'max_iter': (500, 1000)
}

grid_search_pon = GridSearchCV(model,
                           parameters,
                           cv=5,
                           n_jobs=-1 ,
                           scoring='accuracy',
                          verbose=1)

grid_search_pon.fit(X,y)

model_def = grid_search_pon.best_estimator_

pipeline_pon = Pipeline([
    ('vect', tf_vec),
    ('model', model_def)
])

# Guardar modelo:

with open('datafunction/interaction_5.pkl', "wb") as modelo_salida:
    pickle.dump(pipeline_pon, modelo_salida)