import requests
import re
import json
from datetime import datetime

# Ambil data dari website market
market_slug = "btc-updown-5m-1776357600"
url = f"https://polymarket.com/event/{market_slug}"

print(f"Fetching: {url}")

resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
html = resp.text

# Cari data di HTML (biasanya ada di __NEXT_DATA__ atau similar)
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
if next_data_match:
    try:
        data = json.loads(next_data_match.group(1))
        print("=== Found __NEXT_DATA__ ===")

        # Navigate ke market data
        props = data.get('props', {})
        page_props = props.get('pageProps', {})

        print(f"Keys: {list(page_props.keys())}")
        print(f"Data: {json.dumps(page_props, indent=2)[:2000]}...")
    except Exception as e:
        print(f"Error parsing JSON: {e}")

# Cari token IDs di HTML
token_matches = re.findall(r'token_id["\']?\s*[:=]\s*["\']([0-9a-zA-Z]+)["\']', html)
if token_matches:
    print(f"\n=== Found token IDs ===")
    for token in token_matches[:5]:
        print(f"  - {token}")

# Cari condition IDs
condition_matches = re.findall(r'condition["\']?["\']?\s*[:=]\s*["\']([0-9a-zA-Z]+)["\']', html)
if condition_matches:
    print(f"\n=== Found condition IDs ===")
    for cond in condition_matches[:5]:
        print(f"  - {cond}")

# Cari price data
price_matches = re.findall(r'"price"[:\s]+([0-9.]+)', html)
if price_matches:
    print(f"\n=== Found prices ===")
    for price in price_matches[:5]:
        print(f"  - {price}")
