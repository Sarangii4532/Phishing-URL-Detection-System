import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from url_feature_extraction import extract_url_features


# --------------------------------------------------
# 1. Load original dataset
# --------------------------------------------------

file_path = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Number of URLs:", len(df))


# --------------------------------------------------
# 2. Extract features using OUR extractor
# --------------------------------------------------

print("\nExtracting URL features...")
print("This may take a few minutes...")

feature_rows = []
labels = []

for index, row in df.iterrows():

    url = str(row["URL"])

    features = extract_url_features(url)

    feature_rows.append(features)
    labels.append(row["label"])

    if (index + 1) % 10000 == 0:
        print("Processed:", index + 1, "URLs")


# Convert extracted features into DataFrame
X = pd.DataFrame(feature_rows)

y = pd.Series(labels, name="label")


print("\nFeature extraction completed!")

print("Feature dataset shape:", X.shape)


# --------------------------------------------------
# 3. Split dataset
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
# 4. Train Random Forest
# --------------------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# --------------------------------------------------
# 5. Evaluate model
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)


print("\n" + "=" * 55)
print("CONSISTENT URL MODEL RESULTS")
print("=" * 55)

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))


# --------------------------------------------------
# 6. Save model
# --------------------------------------------------

os.makedirs("model", exist_ok=True)

model_path = "model/consistent_url_phishing_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Location:", model_path)

print("\nTraining completed!")
