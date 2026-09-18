import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import joblib


# --------------------------------------------------
# 1. Load cleaned dataset
# --------------------------------------------------

file_path = "dataset/processed_data/cleaned_phishing_dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 2. Separate features and target
# --------------------------------------------------

X = df.drop("label", axis=1)
y = df["label"]


# --------------------------------------------------
# 3. Split dataset into training and testing data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 4. Create machine learning models
# --------------------------------------------------

models = {

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
}


# --------------------------------------------------
# 5. Train and evaluate models
# --------------------------------------------------

results = {}

best_model = None
best_model_name = None
best_f1 = 0


for name, model in models.items():

    print("\nTraining:", name)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_model_name = name


# --------------------------------------------------
# 6. Display comparison
# --------------------------------------------------

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for name, metrics in results.items():

    print("\n", name)

    for metric, value in metrics.items():
        print(metric + ":", round(value, 4))


# --------------------------------------------------
# 7. Save the best model
# --------------------------------------------------

os.makedirs("model", exist_ok=True)

model_path = "model/phishing_url_model.pkl"

joblib.dump(best_model, model_path)

print("\n" + "=" * 60)
print("BEST MODEL:", best_model_name)
print("BEST F1 SCORE:", round(best_f1, 4))
print("Model saved to:", model_path)
print("=" * 60)
