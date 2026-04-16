import requests
import json

# Coba fetch price via CLOB API (yang dipake buat trading)
condition_id = "0x" + format(1776357600, 'x')  # timestamp ke hex
print(f"Condition ID (hex): {condition_id}")

# Coba CLOB price endpoint
clob_url = "https://clob.polymarket.com/markets"

# Try get markets by condition
params = {
    "condition_id": condition_id,
    "closed": "false"
}

print(f"\n=== CLOB markets API ===")
print(f"URL: {clob_url}")
print(f"Params: {params}")

resp = requests.get(clob_url, params=params)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    print(f"Response: {json.dumps(data, indent=2)[:1000]}")
else:
    print(f"Error: {resp.text}")

# Coba alternative: fetch token price langsung
print(f"\n=== Try fetch token IDs ===")
# Dari embed, kita bisa scrape token IDs
# BTC UP/DOWN biasanya punya pattern token ID

# Coba search markets dengan "bitcoin" di CLOB
resp = requests.get("https://clob.polymarket.com/markets", params={
    "search": "bitcoin",
    "limit": 50
})
print(f"Search bitcoin status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    btc_mkts = [m for m in data if 'btc' in m.get('question', '').lower() or 'bitcoin' in m.get('question', '').lower()]
    print(f"BTC markets in CLOB: {len(btc_mkts)}")
    for m in btc_mkts[:5]:
        print(f"  - {m.get('question', '')[:60]}...")
        print(f"    Tokens: {m.get('tokens', [])}")
