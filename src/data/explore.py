import pandas as pd
import numpy as np
import os

def explore_data():
    raw_dir = 'data/raw'
    processed_dir = 'data/processed'
    
    fake_path = os.path.join(raw_dir, 'Fake.csv')
    true_path = os.path.join(raw_dir, 'True.csv')
    
    print("Loading datasets...")
    # Using 'utf-8' and error handling to safely parse CSV files
    try:
        fake_df = pd.read_csv(fake_path, encoding='utf-8')
    except UnicodeDecodeError:
        fake_df = pd.read_csv(fake_path, encoding='latin1')
        
    try:
        true_df = pd.read_csv(true_path, encoding='utf-8')
    except UnicodeDecodeError:
        true_df = pd.read_csv(true_path, encoding='latin1')
    
    # 2. Add binary target label: FAKE = 0, REAL = 1
    fake_df['label'] = 0
    true_df['label'] = 1
    
    # 3. Combine both datasets
    combined_df = pd.concat([fake_df, true_df], ignore_index=True)
    
    print("\n--- DATASET OVERVIEW ---")
    # number of rows and columns
    print(f"Shape (rows, columns): {combined_df.shape}")
    
    # column names
    print(f"Column Names: {list(combined_df.columns)}")
    
    # first 5 rows
    print("\nFirst 5 rows:")
    print(combined_df.head())
    
    # missing values
    print("\nMissing values per column (NaN/Null):")
    print(combined_df.isnull().sum())
    
    # duplicate rows
    duplicate_count = combined_df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicate_count}")
    
    # fake vs real class distribution
    print("\nClass distribution (0 = FAKE, 1 = REAL):")
    print(combined_df['label'].value_counts())
    
    # Check if 'title' and 'text' exist
    if 'title' in combined_df.columns and 'text' in combined_df.columns:
        # missing titles (NaN or empty/whitespace)
        missing_titles = combined_df['title'].isnull().sum() + (combined_df['title'].str.strip() == '').sum()
        
        # missing article text (NaN or empty/whitespace)
        missing_text = combined_df['text'].isnull().sum() + (combined_df['text'].str.strip() == '').sum()
        
        print(f"\nMissing titles (Null or Empty): {missing_titles}")
        print(f"Missing article text (Null or Empty): {missing_text}")
        
        # average title length
        avg_title_len = combined_df['title'].fillna('').astype(str).apply(len).mean()
        # average article length
        avg_text_len = combined_df['text'].fillna('').astype(str).apply(len).mean()
        
        print(f"\nAverage title length (characters): {avg_title_len:.2f}")
        print(f"Average article length (characters): {avg_text_len:.2f}")
    else:
        print("\n'title' and/or 'text' columns are missing. Cannot compute text statistics.")
        
    # 8. Save the combined dataset
    out_path = os.path.join(processed_dir, 'combined_news.csv')
    print(f"\nSaving combined dataset to {out_path} ...")
    combined_df.to_csv(out_path, index=False)
    print("Saved successfully!")

if __name__ == '__main__':
    explore_data()
