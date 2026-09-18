# Phishing URL Detection System

## Overview

The Phishing URL Detection System is a machine learning-based application designed to analyze URLs and classify them as either phishing or legitimate.

The system extracts different URL characteristics and uses a trained machine learning model to make the prediction.

## Features

- URL feature extraction
- Machine learning-based URL classification
- Phishing probability
- Legitimate probability
- Suspicious URL characteristics
- Flask web interface
- Scan history
- Security dashboard
- Recent scan display
- Clear scan history
- Export scan history to CSV
- Download individual scan reports
- Invalid URL validation
## Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- HTML
- CSS
- Machine Learning
- Random Forest

## Project Structure

```text
Phishing-URL-Detection-System
│
├── app.py
├── predict_url.py
├── url_feature_extraction.py
├── scan_history.csv
│
├── model
│   └── consistent_url_phishing_model.pkl
│
├── templates
│   ├── index.html
│   ├── history.html
│   └── dashboard.html
│
└── static
    └── style.css
