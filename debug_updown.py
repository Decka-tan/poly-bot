import requests
import json

resp = requests.get('https://gamma-api.polymarket.com/markets', params={
    'closed': 'false',
    'limit': 200
})

data = resp.json()
print(f'Total markets: {len(data)}')

# Cari Up or Down markets
updown = [m for m in data if 'up or down' in m.get('question', '').lower()]
print(f'Up/Down markets: {len(updown)}')

if updown:
    for m in updown[:10]:
        print(f"\n{m.get('question', '')}")
        print(f"  Active: {m.get('active')}, Closed: {m.get('closed')}")
        print(f"  EndDate: {m.get('endDate', 'N/A')}")
else:
    print("No Up/Down markets found!")
    print("\n=== Looking for time-based markets ===")
    time_mkts = [m for m in data if any(x in m.get('question', '') for x in ['AM', 'PM', ':', 'ET'])]
    print(f'Time-based markets: {len(time_mkts)}')
    for m in time_mkts[:5]:
        print(f"  - {m.get('question', '')[:70]}...")
