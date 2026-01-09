import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from typing import List

MODEL_PATH = "data/model.joblib"

class DocumentClassifier:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
            print(f"Loaded model from {self.model_path}")
        else:
            print("No model found. Please train first.")
            self.pipeline = None

    def train(self, texts: List[str], labels: List[str]):
        """Trains a TF-IDF + Logistic Regression pipeline."""
        print("Training model...")
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
            ('clf', LogisticRegression(random_state=42))
        ])
        self.pipeline.fit(texts, labels)
        self.save_model()
        print("Training complete.")

    def save_model(self):
        if self.pipeline:
            joblib.dump(self.pipeline, self.model_path)
            print(f"Model saved to {self.model_path}")

    def predict(self, text: str) -> str:
        if not self.pipeline:
            # Fallback or error
            return "unknown"
        return self.pipeline.predict([text])[0]

    def predict_proba(self, text: str):
        if not self.pipeline:
             return {}
        probs = self.pipeline.predict_proba([text])[0]
        classes = self.pipeline.classes_
        return dict(zip(classes, probs))
