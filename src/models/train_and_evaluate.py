import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import pickle
import os

def load_data():
    processed_dir = 'data/processed'
    X_train_tfidf = sparse.load_npz(os.path.join(processed_dir, 'X_train_tfidf.npz'))
    X_test_tfidf = sparse.load_npz(os.path.join(processed_dir, 'X_test_tfidf.npz'))
    y_train = np.load(os.path.join(processed_dir, 'y_train.npy'))
    y_test = np.load(os.path.join(processed_dir, 'y_test.npy'))
    
    # We also need the original text for error analysis.
    # Re-split with same random_state=42 and stratify=label to get the exact same test records.
    df = pd.read_csv(os.path.join(processed_dir, 'cleaned_news.csv'))
    _, df_test = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    
    return X_train_tfidf, X_test_tfidf, y_train, y_test, df_test

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def evaluate_model(name, model, X_test, y_test, df_test, reports_dir):
    print(f"\n{'='*40}")
    print(f"Evaluating {name}...")
    
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec_macro = precision_score(y_test, y_pred, average='macro')
    rec_macro = recall_score(y_test, y_pred, average='macro')
    f1_macro = f1_score(y_test, y_pred, average='macro')
    
    print(f"\nAccuracy: {acc:.4f}")
    
    print("\nClassification Report:")
    report = classification_report(y_test, y_pred, target_names=['FAKE (0)', 'REAL (1)'])
    print(report)
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print("Confusion Matrix:")
    print(f"TN: {tn} | FP: {fp}")
    print(f"FN: {fn} | TP: {tp}")
    
    # Error Analysis
    # False Positive: Actual REAL (1) -> Pred FAKE (0)
    fp_mask = (y_test == 1) & (y_pred == 0)
    # False Negative: Actual FAKE (0) -> Pred REAL (1)
    fn_mask = (y_test == 0) & (y_pred == 1)
    
    # Create error dataframe
    errors_df = df_test.copy()
    errors_df['predicted_label'] = y_pred
    
    fp_df = errors_df.loc[fp_mask].copy()
    fp_df['error_type'] = 'False Positive (Actual REAL -> Pred FAKE)'
    
    fn_df = errors_df.loc[fn_mask].copy()
    fn_df['error_type'] = 'False Negative (Actual FAKE -> Pred REAL)'
    
    all_errors = pd.concat([fp_df, fn_df])
    
    error_csv_path = os.path.join(reports_dir, 'error_analysis', f"{name.replace(' ', '_').lower()}_errors.csv")
    all_errors[['title', 'text', 'label', 'predicted_label', 'error_type']].to_csv(error_csv_path, index=False)
    
    print(f"\nSaved {len(all_errors)} misclassified examples to {error_csv_path}")
    
    if len(fp_df) > 0:
        print("\nExample False Positive (Actual REAL, Predicted FAKE):")
        ex_fp = fp_df.iloc[0]
        print(f"Title: {ex_fp['title']}")
        print(f"Text snippet: {ex_fp['text'][:200]}...")
        
    if len(fn_df) > 0:
        print("\nExample False Negative (Actual FAKE, Predicted REAL):")
        ex_fn = fn_df.iloc[0]
        print(f"Title: {ex_fn['title']}")
        print(f"Text snippet: {ex_fn['text'][:200]}...")
    
    return {
        'Model': name,
        'Accuracy': round(acc, 4),
        'Precision': round(prec_macro, 4),
        'Recall': round(rec_macro, 4),
        'F1 Score': round(f1_macro, 4)
    }

def run_pipeline():
    print("Loading datasets and vector features...")
    X_train_tfidf, X_test_tfidf, y_train, y_test, df_test = load_data()
    
    models_dir = 'models'
    reports_dir = 'reports'
    os.makedirs(os.path.join(reports_dir, 'error_analysis'), exist_ok=True)
    
    # Logistic Regression
    print("\nTraining Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_tfidf, y_train)
    save_model(lr, os.path.join(models_dir, 'logistic_regression.pkl'))
    
    # Linear SVM
    print("Training Linear SVM...")
    svm = LinearSVC(C=1.0, random_state=42)
    svm.fit(X_train_tfidf, y_train)
    save_model(svm, os.path.join(models_dir, 'linear_svm.pkl'))
    
    # Evaluate
    results = []
    results.append(evaluate_model("Logistic Regression", lr, X_test_tfidf, y_test, df_test, reports_dir))
    results.append(evaluate_model("Linear SVM", svm, X_test_tfidf, y_test, df_test, reports_dir))
    
    # Comparison
    comparison_df = pd.DataFrame(results)
    comparison_path = os.path.join(reports_dir, 'model_comparison.csv')
    comparison_df.to_csv(comparison_path, index=False)
    
    print(f"\n{'='*40}")
    print("Model Comparison Summary (Macro Averages):")
    print(comparison_df.to_string(index=False))

if __name__ == '__main__':
    run_pipeline()
