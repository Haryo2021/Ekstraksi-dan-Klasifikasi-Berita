import re
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from src.rewriters import rewrite_list_of_sentences

def clean_for_t5(s):
    return s.strip()

def summarize_to_points(text, n_points=3):
    try: 
        sentences = sent_tokenize(text)
    except:
        sentences = re.split(r'(?<=[.!?]) +', text)

    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) == 0:
        return []
    
    if len(sentences) <= n_points:
        clean_points = []
        for s in sentences:
            cleaned_s = clean_for_t5(s)
            res = rewrite_list_of_sentences(cleaned_s)
            clean_points.append(res)
        return clean_points

    indo_stopwords = StopWordRemoverFactory().get_stop_words()
    vectorizer = TfidfVectorizer(stop_words=indo_stopwords)
    try:
        X = vectorizer.fit_transform(sentences)
        scores = np.array(X.mean(axis=1)).ravel()
        top_sentences_indices = scores.argsort()[-n_points:]
        top_sentences = [sentences[i] for i in sorted(top_sentences_indices)] 
    except ValueError:
        top_sentences = sentences[:n_points]

    clean_points = []
    for s in top_sentences:
        cleaned_s = clean_for_t5(s)
        abstractive_point = rewrite_list_of_sentences(cleaned_s)
        clean_points.append(abstractive_point)

    return clean_points