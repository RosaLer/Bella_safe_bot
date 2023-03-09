import os
import numpy as np
import pandas as pd
import re
import ssl
import urllib.request
from bs4 import BeautifulSoup

# NLP
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer



def articulo(url, etiqueta, clase):
    ssl._create_default_https_context = ssl._create_unverified_context

    url = url
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html)
    tags = soup.find_all(etiqueta,class_=clase)
    return tags

def idf_adjustment(X, y, word_adjustments, with_adjustment = False):
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(X)
    X_tfidf = X_tfidf.toarray()
    
    if with_adjustment:
        for word, adjustments in word_adjustments.items():
            for category_id, adjustment in adjustments.items():
                wordindex = vectorizer.vocabulary_.get(word, None)
                if wordindex is not None:
                    for indice, categoria in enumerate(y):
                        if categoria == category_id:
                            X_tfidf[indice,wordindex] += adjustment
    df_valores_tf = pd.DataFrame(X_tfidf, columns = vectorizer.get_feature_names_out())

    return df_valores_tf
