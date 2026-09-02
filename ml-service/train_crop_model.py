"""
Crop Recommendation Model Trainer.
Trains high-precision Random Forest Classifier on Maharashtra Agronomic Dataset (maharashtra_crop_data.csv).
"""
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_maharashtra_model(
    data_path: str = "data/maharashtra_crop_data.csv",
    model_path: str = "models/crop_recommendation.joblib"
):
    base_dir = os.path.dirname(__file__)
    full_data_path = os.path.join(base_dir, data_path)
    full_model_path = os.path.join(base_dir, model_path)

    if not os.path.exists(full_data_path):
        from generate_maharashtra_dataset import generate_maharashtra_dataset
        print("Generating Maharashtra dataset...")
        df = generate_maharashtra_dataset(samples_per_crop=250)
        os.makedirs(os.path.dirname(full_data_path), exist_ok=True)
        df.to_csv(full_data_path, index=False)
    else:
        df = pd.read_csv(full_data_path)

    print(f"Loaded Maharashtra agricultural dataset with {len(df)} records across {df['label'].nunique()} crops.")

    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Random Forest Classifier on Maharashtra dataset...")
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=25,
        min_samples_split=2,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Maharashtra Model Test Accuracy: {acc * 100:.2f}%")

    os.makedirs(os.path.dirname(full_model_path), exist_ok=True)
    payload = {
        'model': model,
        'features': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'],
        'classes': list(model.classes_),
        'accuracy': float(acc),
        'region': 'Maharashtra State (Vidarbha, Marathwada, Western MH, Khandesh, Konkan)'
    }
    joblib.dump(payload, full_model_path)
    print(f"Successfully saved trained model artifact to {full_model_path}")


if __name__ == "__main__":
    train_maharashtra_model()
