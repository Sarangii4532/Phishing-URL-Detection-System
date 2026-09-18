from flask import Flask, render_template, request, send_file, make_response
import joblib
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime
import os
import csv

from url_feature_extraction import extract_url_features

app = Flask(__name__)

scan_history = []

history_file = "scan_history.csv"

# Load previous scan history
if os.path.exists(history_file):
    with open(history_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["phishing_probability"] = float(row["phishing_probability"])
            row["legitimate_probability"] = float(row["legitimate_probability"])
            scan_history.append(row)


# Load trained model
model_path = "model/consistent_url_phishing_model.pkl"
model = joblib.load(model_path)


# Feature order used by the trained model
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


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        # Basic URL validation
        parsed_url = urlparse(url)

        if not url:

            result = {
                "error": "Please enter a URL."
            }

        elif not parsed_url.scheme or not parsed_url.netloc:

            result = {
                "error": "Please enter a valid URL, such as https://example.com"
            }

        else:

            # Extract URL features
            features = extract_url_features(url)

            # Create dataframe
            input_data = pd.DataFrame(
                [[features[f] for f in feature_order]],
                columns=feature_order
            )

            # Make prediction
            prediction = model.predict(input_data)[0]

            # Get probabilities
            probabilities = model.predict_proba(input_data)[0]

            phishing_probability = probabilities[0]
            legitimate_probability = probabilities[1]

            # Suspicious characteristics
            characteristics = []

            if features["IsDomainIP"] == 1:
                characteristics.append("Domain uses an IP address")

            if features["IsHTTPS"] == 0:
                characteristics.append("URL does not use HTTPS")

            if features["NoOfSubDomain"] >= 3:
                characteristics.append("High number of subdomains")

            if features["URLLength"] > 75:
                characteristics.append("Long URL")

            if features["HasObfuscation"] == 1:
                characteristics.append("Possible URL obfuscation")

            if features["NoOfDegitsInURL"] > 5:
                characteristics.append("High number of digits")

            if features["NoOfQMarkInURL"] > 1:
                characteristics.append("Multiple question marks")

            if features["NoOfAmpersandInURL"] > 2:
                characteristics.append("Multiple URL parameters")

            # Store prediction result
            result = {
                "url": url,
                "prediction": "PHISHING" if prediction == 0 else "LEGITIMATE",
                "phishing_probability": round(phishing_probability * 100, 2),
                "legitimate_probability": round(legitimate_probability * 100, 2),
                "characteristics": characteristics
            }

            # Create scan history record
            scan_record = {
                "url": url,
                "prediction": result["prediction"],
                "phishing_probability": result["phishing_probability"],
                "legitimate_probability": result["legitimate_probability"],
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            # Add to memory
            scan_history.append(scan_record)

            # Save to CSV
            file_exists = os.path.exists(history_file)

            with open(
                history_file,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                fieldnames = [
                    "url",
                    "prediction",
                    "phishing_probability",
                    "legitimate_probability",
                    "time"
                ]

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames
                )

                if not file_exists:
                    writer.writeheader()

                writer.writerow(scan_record)

    return render_template("index.html", result=result)


@app.route("/history")
def history():

    return render_template(
        "history.html",
        scan_history=scan_history
    )
@app.route("/clear-history")
def clear_history():

    scan_history.clear()

    with open(history_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "url",
            "prediction",
            "phishing_probability",
            "legitimate_probability",
            "time"
        ])

    return render_template("history.html", scan_history=scan_history)
@app.route("/export-history")
def export_history():

    return send_file(
        history_file,
        as_attachment=True,
        download_name="scan_history.csv",
        mimetype="text/csv"
    )
@app.route("/dashboard")
def dashboard():

    total_scans = len(scan_history)

    phishing_count = 0
    legitimate_count = 0

    for scan in scan_history:

        if scan["prediction"] == "PHISHING":
            phishing_count += 1

        elif scan["prediction"] == "LEGITIMATE":
            legitimate_count += 1

    recent_scans = scan_history[-5:]
    recent_scans = list(reversed(recent_scans))

    return render_template(
        "dashboard.html",
        total_scans=total_scans,
        phishing_count=phishing_count,
        legitimate_count=legitimate_count,
        recent_scans=recent_scans
    )
@app.route("/download-report")
def download_report():

    if not scan_history:
        return "No scan history available."

    latest_scan = scan_history[-1]

    report = f"""
PHISHING URL DETECTION SYSTEM
=============================

SCAN REPORT

URL:
{latest_scan["url"]}

Prediction:
{latest_scan["prediction"]}

Phishing Probability:
{latest_scan["phishing_probability"]}%

Legitimate Probability:
{latest_scan["legitimate_probability"]}%

Scan Time:
{latest_scan["time"]}

=============================
Machine Learning Based URL Security Analysis
"""

    response = make_response(report)
    response.headers["Content-Type"] = "text/plain"
    response.headers["Content-Disposition"] = "attachment; filename=scan_report.txt"

    return response


if __name__ == "__main__":
    app.run(debug=True)

