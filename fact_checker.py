import os
import requests

def search_web(query, num_results=3):
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        return "❌ Missing SERP_API_KEY."

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": num_results
    }

    res = requests.get("https://serpapi.com/search", params=params)
    data = res.json()
    links = []

    for item in data.get("organic_results", []):
        title = item.get("title")
        url = item.get("link")
        if title and url:
            links.append(f"- [{title}]({url})")

    return "\n".join(links) if links else "No relevant sources found."
