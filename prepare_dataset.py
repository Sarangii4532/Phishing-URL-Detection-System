import pandas as pd
import os

# Original dataset
input_file = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

# Load dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Features we will use for machine learning
selected_features = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "URLSimilarityIndex",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "URLCharProb",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasExternalFormSubmit",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfExternalRef",
    "label"
]

# Create a new dataframe with selected features
clean_df = df[selected_features].copy()

# Remove rows containing missing values
clean_df = clean_df.dropna()

# Create processed_data folder
os.makedirs("dataset/processed_data", exist_ok=True)

# Save cleaned dataset
output_file = "dataset/processed_data/cleaned_phishing_dataset.csv"
clean_df.to_csv(output_file, index=False)

print("\nData preparation completed!")
print("Cleaned dataset shape:", clean_df.shape)
print("Saved to:", output_file)

print("\nLabel distribution:")
print(clean_df["label"].value_counts())
