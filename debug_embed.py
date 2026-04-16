import requests
import json
import time

# Coba fetch via embed API
market_slug = "btc-updown-5m-1776357600"
embed_url = f"https://embed.polymarket.com/market?market={market_slug}"

print(f"=== Fetching embed API ===")
print(f"URL: {embed_url}")

resp = requests.get(embed_url)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    print(f"Content type: {resp.headers.get('content-type')}")
    print(f"Response (first 1000 chars): {resp.text[:1000]}")
else:
    print(f"Error: {resp.text}")

# Coba langsung market endpoint
print(f"\n=== Direct market endpoint ===")
market_url = f"https://gamma-api.polymarket.com/markets/{market_slug}"
print(f"URL: {market_url}")

resp = requests.get(market_url)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Market data: {json.dumps(data, indent=2)[:1000]}")
else:
    print(f"Error: {resp.text}")

# Coba search pakai timestamp pattern
print(f"\n=== Search with timestamp pattern ===")
# Generate beberapa timestamp untuk 5-min window ahead
now = int(time.time())
for i in range(1, 6):
    ts = now + (i * 5 * 60)  # 5, 10, 15, 20, 25 menit ke depan
    slug = f"btc-updown-5m-{ts}"
    print(f"Checking: {slug}")
    resp = requests.get(f"https://gamma-api.polymarket.com/markets/{slug}")
    if resp.status_code == 200:
        print(f"  FOUND! Status: {resp.status_code}")
        break
    else:
        print(f"  Not found: {resp.status_code}")
