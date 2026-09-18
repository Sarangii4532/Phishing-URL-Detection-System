import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score
)

import matplotlib.pyplot as plt


# Load cleaned dataset
file_path = "dataset/processed_data/cleaned_phishing_dataset.csv"
df = pd.read_csv(file_path)

# Separate features and label
X = df.drop("label", axis=1)
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("Training Random Forest...")
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Classification Report
print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Phishing", "Legitimate"]
))

# ROC-AUC
auc = roc_auc_score(y_test, y_probability)

print("ROC-AUC Score:", round(auc, 4))


# Create reports folder
os.makedirs("reports", exist_ok=True)


# -----------------------------
# Confusion Matrix Plot
# -----------------------------

plt.figure(figsize=(6, 5))

plt.imshow(cm)

plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

plt.xticks([0, 1], ["Phishing", "Legitimate"])
plt.yticks([0, 1], ["Phishing", "Legitimate"])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j],
                 ha="center",
                 va="center")

plt.tight_layout()

plt.savefig("reports/confusion_matrix.png")

plt.show()


# -----------------------------
# ROC Curve
# -----------------------------

fpr, tpr, thresholds = roc_curve(y_test, y_probability)

plt.figure(figsize=(7, 5))

plt.plot(fpr, tpr)

plt.plot([0, 1], [0, 1], linestyle="--")

plt.title("ROC Curve")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.tight_layout()

plt.savefig("reports/roc_curve.png")

plt.show()


print("\nEvaluation completed successfully!")
print("Reports saved inside the reports folder.")
