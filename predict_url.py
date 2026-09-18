import joblib
import pandas as pd

from url_feature_extraction import extract_url_features


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model_path = "model/consistent_url_phishing_model.pkl"

model = joblib.load(model_path)

print("Phishing URL Detection System")
print("=" * 50)


# --------------------------------------------------
# Get URL from user
# --------------------------------------------------

url = input("\nEnter a URL to analyze: ").strip()


# --------------------------------------------------
# Extract URL features
# --------------------------------------------------

features = extract_url_features(url)

feature_order = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
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
    "IsHTTPS"
]


# Create dataframe
input_data = pd.DataFrame(
    [[features[f] for f in feature_order]],
    columns=feature_order
)


# --------------------------------------------------
# Make prediction
# --------------------------------------------------

prediction = model.predict(input_data)[0]

probabilities = model.predict_proba(input_data)[0]

# Dataset labels:
# 0 = Phishing
# 1 = Legitimate

phishing_probability = probabilities[0]
legitimate_probability = probabilities[1]


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\n" + "=" * 50)
print("ANALYSIS RESULT")
print("=" * 50)

print("URL:", url)

if prediction == 0:
    print("\nPrediction: PHISHING")
    print(
        "Phishing Probability:",
        round(phishing_probability * 100, 2),
        "%"
    )
else:
    print("\nPrediction: LEGITIMATE")
    print(
        "Legitimate Probability:",
        round(legitimate_probability * 100, 2),
        "%"
    )

print(
    "\nPhishing Probability:",
    round(phishing_probability * 100, 2),
    "%"
)

print(
    "Legitimate Probability:",
    round(legitimate_probability * 100, 2),
    "%"
)


# --------------------------------------------------
# Show suspicious characteristics
# --------------------------------------------------

print("\nURL Characteristics:")
print("-" * 50)

if features["IsDomainIP"] == 1:
    print("[!] Domain uses an IP address")

if features["IsHTTPS"] == 0:
    print("[!] URL does not use HTTPS")

if features["NoOfSubDomain"] >= 3:
    print("[!] High number of subdomains")

if features["URLLength"] > 75:
    print("[!] Long URL")

if features["HasObfuscation"] == 1:
    print("[!] Possible URL obfuscation")

if features["NoOfDegitsInURL"] > 5:
    print("[!] High number of digits")

if features["NoOfQMarkInURL"] > 1:
    print("[!] Multiple question marks")

if features["NoOfAmpersandInURL"] > 2:
    print("[!] Multiple URL parameters")

print("\nAnalysis completed.")
