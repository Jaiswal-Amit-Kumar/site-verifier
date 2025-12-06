from urllib.parse import urlparse

def save_screenshot_placeholder(url, shortname):
    """
    Return clean homepage URL (remove query params, anchors)
    """
    parsed = urlparse(url)
    clean_url = f"{parsed.scheme}://{parsed.netloc}/"
    return clean_url
