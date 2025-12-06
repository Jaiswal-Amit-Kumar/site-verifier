from bs4 import BeautifulSoup
import re

def clean_text(text):
    return re.sub(r"\s+", " ", text).lower()

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ")
