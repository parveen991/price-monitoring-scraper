"""
Competitor Price Monitor
Client: GadgetBazaar (electronics retailer)
Delivered: April 2024
Fee: $150

Scrapes competitor prices daily, compares with client's catalog,
flags where client is more expensive.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys

# ---------- 1. Scrape competitor (books.toscrape.com as example) ----------
url = "https://books.toscrape.com"
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching competitor data: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")
products = soup.find_all("article", class_="product_pod")

competitor_data = []
for product in products:
    name = product.h3.a["title"]
    price_text = product.find("p", class_="price_color").text
    # Remove currency symbol and convert to float
    price = float(price_text.replace("£", "").replace("$", "").strip())
    competitor_data.append({"Product": name, "Competitor_Price": price})

competitor_df = pd.DataFrame(competitor_data)

# ---------- 2. Load client prices ----------
try:
    client_df = pd.read_csv("client_prices.csv")
except FileNotFoundError:
    print("client_prices.csv not found. Run generate_client_prices.py first.")
    sys.exit(1)

# ---------- 3. Merge and compare ----------
merged = pd.merge(client_df, competitor_df, on="Product", how="inner")
if merged.empty:
    print("No matching products found between client catalog and competitor site.")
    sys.exit(0)

merged["Price_Difference"] = merged["Client_Price"] - merged["Competitor_Price"]
merged["Status"] = merged["Price_Difference"].apply(
    lambda x: "More Expensive" if x > 0 else ("Cheaper" if x < 0 else "Same")
)

# ---------- 4. Save timestamped report ----------
today = datetime.now().strftime("%Y-%m-%d")
filename = f"price_comparison_{today}.csv"
merged.to_csv(filename, index=False)

print(f"Report saved: {filename}")
# Quick summary
more_expensive = merged[merged["Status"] == "More Expensive"]
if not more_expensive.empty:
    print(f"ALERT: Client is more expensive on {len(more_expensive)} products:")
    for _, row in more_expensive.iterrows():
        print(f"  - {row['Product']}: Client ${row['Client_Price']} vs Competitor ${row['Competitor_Price']} (diff +${row['Price_Difference']:.2f})")
else:
    print("Client prices are competitive.")
