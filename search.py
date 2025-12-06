from ddgs import DDGS

def search(query, max_results=10):
    urls = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                if 'href' in r:
                    urls.append(r['href'])
        return urls
    except Exception as e:
        print(f"Search error: {e}")
        return []
