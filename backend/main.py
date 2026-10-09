from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import sys
import os

# Add parent directory to path so src can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.predict import NewsPredictor

# Global predictor instance
predictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global predictor
    print("Initializing Fake News Detection Models...")
    predictor = NewsPredictor(model_dir=os.path.join(os.path.dirname(__file__), '..', 'models'))
    print("Models loaded successfully.")
    yield
    # Shutdown
    print("Shutting down API...")

app = FastAPI(title="Fake News Detection API", lifespan=lifespan)

# Enable CORS for future React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    title: str
    text: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.post("/predict")
def predict_news(request: PredictRequest):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Handle empty string inputs safely
    if not request.title.strip() and not request.text.strip():
        raise HTTPException(status_code=400, detail="Both title and text cannot be completely empty.")
    
    try:
        result = predictor.predict(request.title, request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/analytics")
def get_analytics():
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    comp_file = os.path.join(reports_dir, 'model_comparison.csv')
    if not os.path.exists(comp_file):
        raise HTTPException(status_code=404, detail="Analytics report not found")
    
    import pandas as pd
    df = pd.read_csv(comp_file)
    models = []
    for _, row in df.iterrows():
        models.append({
            "model": row["Model"],
            "accuracy": float(row["Accuracy"]),
            "precision": float(row["Precision"]),
            "recall": float(row["Recall"]),
            "f1_score": float(row["F1 Score"]),
            "accuracy_pct": f"{row['Accuracy']*100:.2f}%",
            "precision_pct": f"{row['Precision']*100:.2f}%",
            "recall_pct": f"{row['Recall']*100:.2f}%",
            "f1_pct": f"{row['F1 Score']*100:.2f}%",
            "is_deployed": (row["Model"] == "Linear SVM")
        })
    return {
        "dataset_overview": {
            "total_cleaned": 44058,
            "training_articles": 35246,
            "test_articles": 8812,
            "fake_articles": 22848,
            "real_articles": 21210,
            "split_ratio": "80% Train / 20% Test (Stratified)"
        },
        "model_comparison": models,
        "deployment_selection": {
            "selected_model": "Linear SVM",
            "rationale": "Linear SVM was selected because it achieved the strongest overall performance on the held-out test set.",
            "evaluation_scope": "Evaluated on 8,812 held-out test articles.",
            "disclaimer": "These metrics reflect evaluation on the held-out test dataset and should not be assumed to represent general real-world accuracy on uncurated internet distributions."
        }
    }

@app.get("/error-analysis")
def get_error_analysis():
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    errors_file = os.path.join(reports_dir, 'error_analysis', 'linear_svm_errors.csv')
    if not os.path.exists(errors_file):
        raise HTTPException(status_code=404, detail="Error analysis report not found")
    
    import pandas as pd
    df = pd.read_csv(errors_file)
    examples = []
    for idx, row in df.iterrows():
        examples.append({
            "id": idx + 1,
            "title": str(row["title"]),
            "text": str(row["text"]),
            "actual_label": "REAL" if int(row["label"]) == 1 else "FAKE",
            "predicted_label": "REAL" if int(row["predicted_label"]) == 1 else "FAKE",
            "error_type": str(row["error_type"]),
            "is_fp": "False Positive" in str(row["error_type"]),
            "is_fn": "False Negative" in str(row["error_type"])
        })
    return {
        "confusion_matrix": {
            "true_negative": 4557,
            "false_positive": 13,
            "false_negative": 7,
            "true_positive": 4235,
            "total_test_samples": 8812
        },
        "summary": {
            "false_positives": 13,
            "false_negatives": 7,
            "total_errors": 20
        },
        "explanations": {
            "true_negative": "Fake article correctly classified as Fake.",
            "true_positive": "Real article correctly classified as Real.",
            "false_positive": "Real article incorrectly classified as Fake.",
            "false_negative": "Fake article incorrectly classified as Real.",
            "analytical_insight_fp": "False positives may occur when legitimate news uses sensational, emotional, or strongly opinionated language that resembles patterns found in fake-news training examples.",
            "analytical_insight_fn": "False negatives may occur when fake articles imitate formal journalistic language, use real-world entities, or discuss genuine events while presenting misleading claims.",
            "note": "These are model-error interpretations, not proven causal explanations."
        },
        "errors": examples
    }
