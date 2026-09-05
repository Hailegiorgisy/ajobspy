import requests
import json
from bs4 import BeautifulSoup

url = "https://ethiojobs.net/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')

next_data_script = soup.select_one("script#__NEXT_DATA__")
if next_data_script:
    print("Found __NEXT_DATA__ script tag!")
    try:
        data = json.loads(next_data_script.string)
        print("Successfully parsed JSON payload.")
        # Let's inspect the top-level keys of pageProps
        page_props = data.get("props", {}).get("pageProps", {})
        print("Keys in pageProps:", list(page_props.keys()))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
else:
    print("No __NEXT_DATA__ tag found. Let's inspect all link tags instead.")
    links = [a.get('href') for a in soup.select("a[href]") if a.get('href')]
    print(f"Total links found on page: {len(links)}")
    print("Sample links:", links[:15])