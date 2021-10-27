import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def get_features(logs, gram, min_d):
    vectorizer = CountVectorizer(ngram_range=(gram,gram),min_df=min_d,stop_words='english')
    tf = vectorizer.fit_transform(logs)
    
    transformer = TfidfTransformer()
    tfidf_vectors = transformer.fit_transform(tf)
    
    return tfidf_vectors


