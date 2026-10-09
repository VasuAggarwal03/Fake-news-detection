import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os

def get_tfidf_vectorizer(max_features=50000, ngram_range=(1, 2), min_df=5, max_df=0.7, sublinear_tf=True):
    """
    Returns a configured TfidfVectorizer suitable for news classification.
    """
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf
    )

def save_vectorizer(vectorizer, path):
    """
    Saves the trained vectorizer to a pickle file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(vectorizer, f)

def load_vectorizer(path):
    """
    Loads a trained vectorizer from a pickle file.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)
