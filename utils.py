import re
import hashlib
import requests

API_URL = "https://api.pwnedpasswords.com/range/"

def check_strength(password: str) -> str:
    score = 0
    if len(password) >= 12:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score in (3, 4):
        return "Medium"
    else:
        return "Strong"
    
#I use HIBP(Have I Been Pwned)
def check_breach(password: str) -> int:
    #String password is made into a hash password (k-anonymity: vi sender kun prefix)
    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]

    #Find all suffix that match prefix 
    response = requests.get(API_URL + prefix, headers={"User-Agent": "HenrikPasswordChecker"}, timeout=10)
    response.raise_for_status()

    #See if our suffix exists 
    for line in response.text.splitlines():
        h, count = line.split(":")
        if h == suffix:
            return int(count)
    return 0