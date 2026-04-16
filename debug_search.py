import requests
import json

# Coba search langsung
search_terms = ["Bitcoin", "bitcoin", "BTC", "btc"]

for term in search_terms:
    print(f"\n=== Searching: '{term}' ===")
    resp = requests.get('https://gamma-api.polymarket.com/markets', params={
        'search': term,
        'closed': 'false',
        'limit': 50
    })
    data = resp.json()
    print(f"Found: {len(data)} markets")

    for m in data[:3]:
        print(f"  - {m.get('question', '')[:60]}...")

# Coba cek market by specific condition ID (kalau punya dari history)
print("\n=== Checking bet history ===")
try:
    with open('logs/bets.csv', 'r') as f:
        lines = f.readlines()
        if len(lines) > 1:
            last_bet = lines[-1].split(',')
            print(f"Last bet market_id: {last_bet[3] if len(last_bet) > 3 else 'N/A'}")
except:
    print("No bet history found")
