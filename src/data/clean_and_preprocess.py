import pandas as pd
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.preprocessing.text_cleaner import clean_text

def run_cleaning_pipeline():
    processed_dir = 'data/processed'
    input_path = os.path.join(processed_dir, 'combined_news.csv')
    output_path = os.path.join(processed_dir, 'cleaned_news.csv')
    
    print("Loading combined dataset...")
    df = pd.read_csv(input_path)
    
    initial_rows = len(df)
    
    # 1. Remove exact duplicate rows
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()
    
    # 2. Handle missing/empty article text
    # Find rows where text is null or just whitespace
    missing_text_mask = df['text'].isnull() | (df['text'].str.strip() == '')
    missing_text_count = missing_text_mask.sum()
    
    # Remove those records
    df = df[~missing_text_mask].copy()
    
    # 3. Verify title values are valid (remove if missing)
    missing_title_mask = df['title'].isnull() | (df['title'].str.strip() == '')
    df = df[~missing_title_mask].copy()
    
    # 4. Create new column `content`
    # Ensure no NaN issues when concatenating
    df['content'] = df['title'].fillna('') + " " + df['text'].fillna('')
    
    # 5. Keep only the useful columns
    df = df[['title', 'text', 'subject', 'date', 'label', 'content']]
    
    final_rows = len(df)
    
    # 6. Save the cleaned dataset
    print(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*40)
    print("--- DATA CLEANING REPORT ---")
    print(f"Rows before cleaning: {initial_rows}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Missing-text rows removed: {missing_text_count}")
    print(f"Rows after cleaning: {final_rows}")
    print("\nFinal FAKE/REAL distribution:")
    print(df['label'].value_counts())
    print("="*40)
    
    print("\n--- NLP PREPROCESSING PREVIEW ---")
    # Sample a few records for preview
    preview_samples = df.sample(3, random_state=42)
    for idx, row in preview_samples.iterrows():
        original = row['content']
        preprocessed = clean_text(original)
        
        print(f"\n[Record ID: {idx}] - Class: {'REAL' if row['label'] == 1 else 'FAKE'}")
        # Show first 300 chars of original vs preprocessed to highlight changes
        print(f"ORIGINAL:\n{original[:300]}...")
        print(f"PREPROCESSED:\n{preprocessed[:300]}...")

if __name__ == '__main__':
    run_cleaning_pipeline()
