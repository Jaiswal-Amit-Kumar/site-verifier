from urllib.parse import urlparse
from extractor import clean_text

# Sites to ignore
BLACKLIST = [
    "cnews.ru", "audit-it.ru", "raexpert.ru", "spark-interfax.ru", "znanierussia.ru"
]

# TLD preference
PREFERRED_RU_TLDS = [".ru"]
PREFERRED_GLOBAL_TLDS = [".com", ".org", ".net"]

def is_blacklisted(url):
    domain = urlparse(url).netloc.lower()
    return any(b in domain for b in BLACKLIST)

def is_official_domain(url, shortname):
    domain = urlparse(url).netloc.lower()
    return shortname.lower() in domain

def tld_score(url, is_russian):
    domain = urlparse(url).netloc.lower()
    if is_russian and any(domain.endswith(tld) for tld in PREFERRED_RU_TLDS):
        return 30
    if not is_russian and any(domain.endswith(tld) for tld in PREFERRED_GLOBAL_TLDS):
        return 30
    return 0

def compute_score(text, company, url, is_russian=True):
    score = 0
    matches = []

    t = clean_text(text)
    shortname = clean_text(company["ShortName"])
    name = clean_text(company["Name"])

    if name in t:
        score += 50
        matches.append("Name in Text")

    if shortname in clean_text(url):
        score += 50
        matches.append("ShortName in URL")

    if is_official_domain(url, shortname):
        score += 50
        matches.append("Official Domain")

    score += tld_score(url, is_russian)

    return score, list(set(matches))
