import pandas as pd
from sklearn.model_selection import train_test_split
from scipy import sparse
import numpy as np
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.features.tfidf import get_tfidf_vectorizer, save_vectorizer
from src.preprocessing.text_cleaner import clean_text

def run_extraction():
    processed_dir = 'data/processed'
    input_path = os.path.join(processed_dir, 'cleaned_news.csv')
    
    print("Loading cleaned dataset...")
    df = pd.read_csv(input_path)
    
    # Ensure content is string
    df['content'] = df['content'].fillna('').astype(str)
    
    # Apply text cleaning from Phase 4 to the entire content column
    print("Applying text preprocessing to all content. This might take a minute...")
    df['clean_content'] = df['content'].apply(clean_text)
    
    # PHASE 5 - TRAIN/TEST SPLIT
    print("\n--- PHASE 5: DATA SPLITTING ---")
    X = df['clean_content']
    y = df['label']
    
    # Split using stratify to maintain class distribution, fixed random_state for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}")
    
    print("\nTraining set distribution (0=FAKE, 1=REAL):")
    print(y_train.value_counts())
    
    print("\nTesting set distribution (0=FAKE, 1=REAL):")
    print(y_test.value_counts())
    
    # PHASE 6 - TF-IDF
    print("\n--- PHASE 6: TF-IDF EXTRACTION ---")
    print("Initializing TF-IDF Vectorizer...")
    vectorizer = get_tfidf_vectorizer(
        max_features=50000, 
        ngram_range=(1, 2), 
        min_df=5, 
        max_df=0.7
    )
    
    print("Fitting vectorizer on training data and transforming...")
    # CRITICAL DATA-LEAKAGE RULE: fit_transform ONLY on training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    print("Transforming testing data using the already-fitted vectorizer...")
    # CRITICAL DATA-LEAKAGE RULE: transform ONLY on test data (never fit)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"\nTF-IDF Matrix shape for training: {X_train_tfidf.shape}")
    print(f"TF-IDF Matrix shape for testing: {X_test_tfidf.shape}")
    
    feature_names = vectorizer.get_feature_names_out()
    print(f"Vocabulary size: {len(feature_names)}")
    
    # Show a few example features to verify unigrams/bigrams
    print(f"\nExample feature names: {list(feature_names[5000:5010])}")
    
    # Save the vectorizer
    model_dir = 'models'
    vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
    print(f"\nSaving vectorizer to {vectorizer_path}...")
    save_vectorizer(vectorizer, vectorizer_path)
    
    # Save the split data (sparse matrices and arrays) for the upcoming training phase
    print("Saving transformed matrices and labels for model training...")
    sparse.save_npz(os.path.join(processed_dir, 'X_train_tfidf.npz'), X_train_tfidf)
    sparse.save_npz(os.path.join(processed_dir, 'X_test_tfidf.npz'), X_test_tfidf)
    np.save(os.path.join(processed_dir, 'y_train.npy'), y_train.values)
    np.save(os.path.join(processed_dir, 'y_test.npy'), y_test.values)
    
    print("Done!")

if __name__ == '__main__':
    run_extraction()
