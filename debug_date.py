import requests
from datetime import datetime, timedelta

# Coba search by date
today = datetime.now()
tomorrow = today + timedelta(days=1)

searches = [
    f"April {today.day}",
    f"April {tomorrow.day}",
    f"{today.strftime('%B')} {today.day}",
    f"{today.day}",
]

for search_term in searches:
    print(f"\n=== Searching: '{search_term}' ===")
    resp = requests.get('https://gamma-api.polymarket.com/markets', params={
        'search': search_term,
        'closed': 'false',
        'limit': 50
    })
    data = resp.json()
    updown = [m for m in data if 'up or down' in m.get('question', '').lower() and 'btc' in m.get('question', '').lower()]
    print(f"Total: {len(data)}, BTC Up/Down: {len(updown)}")
    for m in updown[:3]:
        print(f"  - {m.get('question', '')}")

# Coba semua markets, cari yang ada "AM" atau "PM" di title
print("\n=== All markets with time in title ===")
resp = requests.get('https://gamma-api.polymarket.com/markets', params={
    'closed': 'false',
    'limit': 500
})
data = resp.json()
time_markets = [m for m in data if any(x in m.get('question', '') for x in ['AM', 'PM', ':', 'ET'])]
print(f"Time-based markets: {len(time_markets)}")
for m in time_markets[:10]:
    print(f"  - {m.get('question', '')[:70]}...")
