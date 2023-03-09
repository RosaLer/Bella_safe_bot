import os
import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

#Función para tokenizar y lematizar:

my_stop_words = {"empezar", "micro", "año", "x", "am", "rosa", 
                 "mª","martín", "a", "scielo", "serie", "podcasts", "pubcats", "d", 
                    "universida", "activ", "invest", "dtype", "q", "Name", "difer", "aa", 
                    "wwwemergencyphysiciansorg", "…", "—", "abler", "él", "links", "the","of", "about"}

stop_en = stopwords.words('english')

# Stop_word personalizadas y unidas a la bolsa existente:

stop_words = STOP_WORDS.union(my_stop_words).union(stop_en)

nlp = spacy.load('es_core_news_sm')

def token_lemma_list(text):
    model = nlp(text)
    lemmas = [token.lemma_ for token in model if not token.is_stop]
    return [lemma for lemma in lemmas if lemma not in stop_words]

def token_lemma_str(text):
    model = nlp(text)
    lemmas = [token.lemma_ for token in model if not token.is_stop]
    return ' '.join([lemma for lemma in lemmas if lemma not in stop_words])


def plot_wordcloud(text, mask=None, max_words=300, max_font_size=100, figure_size=(24.0,16.0), 
                   title = None, title_size=40, image_color=False):

    wordcloud = WordCloud(background_color='white',
                    stopwords = stop_words,
                    max_words = max_words,
                    max_font_size = max_font_size,
                    width=800, 
                    height=400,
                    mask = mask)
    wordcloud.generate(str(text))
    
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,  
                                  'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'black', 
                                  'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()  