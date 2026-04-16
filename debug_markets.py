import requests
import json

resp = requests.get('https://gamma-api.polymarket.com/markets', params={
    'closed': 'false',
    'limit': 100
})

data = resp.json()
print(f'Total markets: {len(data)}')

# Cari BTC markets
btc = [m for m in data if 'btc' in m.get('question', '').lower() or 'bitcoin' in m.get('question', '').lower()]
print(f'BTC markets: {len(btc)}')

if btc:
    for m in btc[:5]:
        print(f"  - {m.get('question', '')[:60]}...")
        print(f"    Active: {m.get('active')}, Closed: {m.get('closed')}")
else:
    print("No BTC markets found!")
    print("\n=== First 5 markets ===")
    for m in data[:5]:
        print(f"  - {m.get('question', '')[:60]}...")
