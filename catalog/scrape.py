import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

assessments = []

cards = soup.find_all("a")

for card in cards:
    title = card.get_text(strip=True)
    href = card.get("href")

    if title and href:
        assessments.append({
            "name": title,
            "url": href if href.startswith("http") else "https://www.shl.com" + href,
            "description": title
        })

with open("shl_catalog.json", "w") as f:
    json.dump(assessments, f, indent=2)

print("Saved catalog")