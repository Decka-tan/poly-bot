import requests
import json

# Coba alternative endpoints
endpoints = [
    ('Search BTC 5 min', 'https://gamma-api.polymarket.com/markets', {'search': 'Bitcoin Up or Down - 5 Minutes', 'closed': 'false', 'limit': 50}),
    ('Search 5 min', 'https://gamma-api.polymarket.com/markets', {'search': '5 Minutes', 'closed': 'false', 'limit': 50}),
    ('Search Up or Down', 'https://gamma-api.polymarket.com/markets', {'search': 'Up or Down', 'closed': 'false', 'limit': 50}),
    ('All closed=false', 'https://gamma-api.polymarket.com/markets', {'closed': 'false', 'limit': 300}),
    ('WithTag=crypto', 'https://gamma-api.polymarket.com/markets', {'closed': 'false', 'tag': 'crypto', 'limit': 100}),
]

for name, url, params in endpoints:
    print(f"\n=== {name} ===")
    resp = requests.get(url, params=params)
    data = resp.json()
    if isinstance(data, dict):
        data = data.get('markets', data.get('data', []))
    print(f"Total: {len(data)}")

    btc = [m for m in data if 'btc' in m.get('question', '').lower() or 'bitcoin' in m.get('question', '').lower()]
    print(f"BTC markets: {len(btc)}")
    for m in btc[:3]:
        print(f"  - {m.get('question', '')[:60]}...")
