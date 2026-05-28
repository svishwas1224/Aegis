
"""
Train a simple dark pattern detection ML model using scikit-learn
"""
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ------------------------------
# 1. Create synthetic labeled dataset (keyword-based with better examples)
# ------------------------------
dark_pattern_examples = [
    "Only 2 left! Hurry! Limited time offer!",
    "This offer expires in 10 minutes! Don't miss out!",
    "You must accept all cookies to continue browsing",
    "Limited time only! Sale ends tonight!",
    "Almost gone! Last chance to buy!",
    "Check this box if you don't want to unsubscribe from our newsletter",
    "Pre-selected: Subscribe to our weekly newsletter",
    "You might also like this amazing deal!",
    "Cancellation requires phone call only",
    "Auto-renewal enabled by default",
    "Only 3 spots remaining! Reserve now!",
    "Hurry sale ends at midnight!",
    "Limited stock availability!",
    "Check this to not receive promotional emails",
    "You must agree to our terms to proceed",
    "Subscribe now and get a free gift*",
    "*Free gift requires minimum purchase of $50+",
    "Only 1 left in your size!",
    "Don't miss this exclusive offer!",
    "Act now before it's too late!",
    "Offer valid only for next 5 customers",
    "Countdown: 3:45 remaining!"
]

safe_examples = [
    "Welcome to our website",
    "Here is our complete product catalog",
    "Thank you for your recent purchase",
    "Your order has been shipped successfully",
    "Please read our terms of service carefully",
    "Contact us if you have any questions or concerns",
    "Learn more about our products and services",
    "Read our updated privacy policy",
    "Your new account has been created",
    "Here's how to contact our customer support",
    "About our company and mission",
    "Detailed shipping information",
    "Easy returns and exchange policy",
    "Frequently asked questions (FAQ)",
    "Help center and troubleshooting",
    "Complete product specifications",
    "Genuine customer reviews and ratings",
    "Our company's history and values",
    "Size guide and measurement info",
    "Contact information and store locations",
    "Product warranty information",
    "How to place an order",
    "Payment methods we accept"
]

# Create labeled data (1 = dark pattern, 0 = safe)
X = dark_pattern_examples + safe_examples
y = [1] * len(dark_pattern_examples) + [0] * len(safe_examples)

# ------------------------------
# 2. Train ML model
# ------------------------------
print("Training ML model...")

# Create pipeline: TF-IDF vectorizer + Logistic Regression
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))),
    ('classifier', LogisticRegression(C=0.5))
])

# Train
model_pipeline.fit(X, y)

# Quick accuracy check
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)

print("\nModel performance on test set:")
print(classification_report(y_test, y_pred))

# ------------------------------
# 3. Save model
# ------------------------------
import os
os.makedirs("data", exist_ok=True)
model_path = os.path.join("data", "dark_pattern_model.pkl")
with open(model_path, 'wb') as f:
    pickle.dump(model_pipeline, f)

print(f"\n✅ Model saved to {model_path}")

# Quick test prediction
test_texts = [
    "Only 1 left! Hurry!",
    "Welcome to our store",
    "You must accept all cookies to continue",
    "Thank you for your order"
]
predictions = model_pipeline.predict(test_texts)
for text, pred in zip(test_texts, predictions):
    status = "DARK PATTERN" if pred == 1 else "SAFE"
    print(f"\nTest: '{text}' → {status}")
