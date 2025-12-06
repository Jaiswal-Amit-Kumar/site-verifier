import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from search import search
from crawler import fetch_page
from extractor import html_to_text
from matcher import compute_score, is_blacklisted, is_official_domain
from utils import save_screenshot_placeholder

MAX_THREADS = 10  # Adjust for your CPU/network

# Global cache: URL -> HTML text
URL_CACHE = {}

def score_url(company, url, is_russian):
    if is_blacklisted(url):
        return None

    # Check cache
    if url in URL_CACHE:
        html = URL_CACHE[url]
    else:
        html = fetch_page(url)
        URL_CACHE[url] = html

    if not html:
        return None

    text = html_to_text(html)
    score, matches = compute_score(text, company, url, is_russian)
    return url, score, matches

def verify_company(company):
    is_russian = any('а' <= c <= 'я' or 'А' <= c <= 'Я' for c in company['Name'])
    query = f"{company['Name']} официальный сайт" if is_russian else company['Name']
    urls = search(query, max_results=10)
    if not urls and is_russian:
        query = company['Name']
        urls = search(query, max_results=10)

    print(f"Query: {query} -> Found {len(urls)} URLs")
    if not urls:
        return "NOT FOUND", [], 0, ""

    best_score = 0
    best_url = ""
    best_matches = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {executor.submit(score_url, company, url, is_russian): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if result is None:
                continue
            url, score, matches = result

            # Short-circuit official domain + ShortName
            if "Official Domain" in matches and "ShortName in URL" in matches:
                clean_url = save_screenshot_placeholder(url, company["ShortName"])
                return url, matches, score, clean_url

            if score > best_score:
                best_score = score
                best_url = url
                best_matches = matches

    if best_score == 0:
        return "NOT FOUND", [], 0, ""

    clean_url = save_screenshot_placeholder(best_url, company["ShortName"])
    return best_url, best_matches, best_score, clean_url

def main():
    df = pd.read_excel("input.xlsx")
    results = []

    for idx, company in df.iterrows():
        print(f"Processing: {company['Name']}")
        website, matches, score, screenshot = verify_company(company)
        results.append({
            "company": company["Name"],
            "website": website,
            "matches": ", ".join(matches),
            "score": score,
            "screenshot": screenshot
        })

    out_df = pd.DataFrame(results)
    out_df.to_excel("output/results.xlsx", index=False)
    print("Saved output/results.xlsx")

if __name__ == "__main__":
    main()
