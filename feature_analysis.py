import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Load cleaned dataset
file_path = "dataset/processed_data/cleaned_phishing_dataset.csv"
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# Separate features and target
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
print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# Calculate feature importance
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)


# Display all features
print("\nFeature Importance:")
print(importance.to_string(index=False))


# Display top 15 features
print("\n" + "=" * 50)
print("TOP 15 FEATURES")
print("=" * 50)

print(importance.head(15).to_string(index=False))


# Save feature importance results
importance.to_csv(
    "reports/feature_importance.csv",
    index=False
)


# Plot top 15 features
top_features = importance.head(15)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 15 Features Used by Random Forest")

plt.tight_layout()

plt.savefig("reports/feature_importance.png")

plt.show()


print("\nFeature analysis completed!")
print("Saved:")
print("reports/feature_importance.csv")
print("reports/feature_importance.png")
