from urllib.parse import urlparse
import re


def extract_url_features(url):

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc

    # Remove username/password if present
    if "@" in domain:
        domain = domain.split("@")[-1]

    # Remove port number
    domain = domain.split(":")[0]

    # URL length
    url_length = len(url)

    # Domain length
    domain_length = len(domain)

    # Check whether domain is an IP address
    is_domain_ip = 1 if re.match(
        r"^\d{1,3}(\.\d{1,3}){3}$",
        domain
    ) else 0

    # HTTPS
    is_https = 1 if parsed.scheme == "https" else 0

    # Number of subdomains
    domain_parts = domain.split(".")
    no_of_subdomain = max(0, len(domain_parts) - 2)

    # Obfuscation-related features
    suspicious_chars = ["@", "%", "\\"]

    no_of_obfuscated_char = sum(
        url.count(char) for char in suspicious_chars
    )

    has_obfuscation = 1 if no_of_obfuscated_char > 0 else 0

    obfuscation_ratio = (
        no_of_obfuscated_char / url_length
        if url_length > 0 else 0
    )

    # Letters
    no_of_letters = sum(c.isalpha() for c in url)

    letter_ratio = (
        no_of_letters / url_length
        if url_length > 0 else 0
    )

    # Digits
    no_of_digits = sum(c.isdigit() for c in url)

    digit_ratio = (
        no_of_digits / url_length
        if url_length > 0 else 0
    )

    # Special URL characters
    no_of_equals = url.count("=")
    no_of_qmark = url.count("?")
    no_of_ampersand = url.count("&")

    special_characters = "=?:;&%_@#$!"
    
    no_of_other_special_chars = sum(
        url.count(char) for char in special_characters
    )

    special_char_ratio = (
        no_of_other_special_chars / url_length
        if url_length > 0 else 0
    )

    # Create feature dictionary
    features = {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "TLDLength": len(domain_parts[-1]) if domain_parts else 0,
        "NoOfSubDomain": no_of_subdomain,
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": no_of_obfuscated_char,
        "ObfuscationRatio": obfuscation_ratio,
        "NoOfLettersInURL": no_of_letters,
        "LetterRatioInURL": letter_ratio,
        "NoOfDegitsInURL": no_of_digits,
        "DegitRatioInURL": digit_ratio,
        "NoOfEqualsInURL": no_of_equals,
        "NoOfQMarkInURL": no_of_qmark,
        "NoOfAmpersandInURL": no_of_ampersand,
        "NoOfOtherSpecialCharsInURL": no_of_other_special_chars,
        "SpacialCharRatioInURL": special_char_ratio,
        "IsHTTPS": is_https
    }

    return features


# --------------------------------------------------
# Test the feature extractor
# --------------------------------------------------

if __name__ == "__main__":

    test_url = "https://www.example.com/login"

    features = extract_url_features(test_url)

    print("URL:")
    print(test_url)

    print("\nExtracted Features:")
    
    for feature, value in features.items():
        print(f"{feature}: {value}")
