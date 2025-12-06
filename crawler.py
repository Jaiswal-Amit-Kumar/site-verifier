import requests

def fetch_page(url):
    """Fetch HTML content of a URL"""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None
