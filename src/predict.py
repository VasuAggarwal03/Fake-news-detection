import os
import pickle
import sys

# Ensure src modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.preprocessing.text_cleaner import clean_text

class NewsPredictor:
    def __init__(self, model_dir='models'):
        self.vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
        self.model_path = os.path.join(model_dir, 'linear_svm.pkl')
        
        # Load vectorizer
        with open(self.vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
            
        # Load model
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, title: str, text: str) -> dict:
        # Handle empty gracefully
        if title is None:
            title = ""
        if text is None:
            text = ""
            
        # 1. Combine title and article text (same as training)
        content = title + " " + text
        
        # 2. Apply the SAME text preprocessing function
        cleaned_content = clean_text(content)
        
        # 3. Transform using already fitted vectorizer
        features = self.vectorizer.transform([cleaned_content])
        
        # 4. Predict using already trained Linear SVM
        pred_label = self.model.predict(features)[0]
        decision_score = self.model.decision_function(features)[0]
        
        prediction_str = "REAL" if pred_label == 1 else "FAKE"
        
        # 5. Return dict
        return {
            "prediction": prediction_str,
            "model": "Linear SVM",
            "decision_score": float(decision_score)
        }
