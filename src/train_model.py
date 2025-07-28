
# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================



import os, joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# pdf_parser is not directly used in this main function, but often useful for training scripts
# from src.round1a.pdf_parser import parse_spans
from src.round1a.feature_extractor import extract_features
from src.utils.file_io import read_annotations

def main():
    print("Loading annotations for training...")
    df = read_annotations()

    # Calculate median body font size (assuming label 0 is body text)
    # Check if there's any body text to avoid issues with empty selections
    if 0 in df['label'].values:
        median_body = df[df.label==0]["font_size"].median()
    else:
        print("Warning: No '0' (normal body) labels found in annotations. Median body font size will be set to 1.0. This may affect feature quality.")
        median_body = 1.0 # Default or handle this case appropriately

    spans = df.to_dict("records")
    print(f"Extracting features for {len(spans)} spans...")
    X = extract_features(spans, median_body)
    y = df["label"].values

    print("Splitting data into training and validation sets...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42)

    print("Training RandomForestClassifier model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # Use all available CPU cores
    clf.fit(X_train, y_train)
    
    print("\nModel performance on validation set:")
    print(classification_report(y_val, clf.predict(X_val), digits=3))

    # Save the trained model and the median_body font size
    os.makedirs("models", exist_ok=True)
    model_output_path = "models/heading_model.joblib"
    joblib.dump({"model":clf, "median_body":float(median_body)}, model_output_path)
    print(f"\nModel saved → {model_output_path}")


# =========================BitHive===============================
# ===   TEAM MEMBERS:                   =========================
# ===   -> LAKSHYA PRAJAPATI            =========================
# ===   -> REBANT PRATAP SINGH          =========================
# ===   -> SATYAJIT SAHOO               =========================
# ===============================================================