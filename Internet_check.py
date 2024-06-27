import requests

def Internet_check():
    try:
        requests.get("https://www.google.com",timeout=5)
        return True
    except requests.ConnectionError:
        print("wait for the internet to come back...")
        return False