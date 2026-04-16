import requests
import re
import json

url = "https://polymarket.com/event/btc-updown-5m-1776357600"
resp = requests.get(url)
html = resp.text

# Extract __NEXT_DATA__
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
if not next_data_match:
    print("No __NEXT_DATA__ found!")
    exit(1)

data = json.loads(next_data_match.group(1))
dehydrated = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {})

# Parse queries
queries = dehydrated.get('queries', [])
print(f"Total queries: {len(queries)}")

for query in queries:
    state = query.get('state', {})
    if not isinstance(state, dict):
        continue

    # Cari query dengan market data
    query_data = state.get('data', [])

    if isinstance(query_data, list):
        for item in query_data:
            if isinstance(item, dict):
                # Cek item dengan token, condition_id, atau question
                if any(k in item for k in ['token_id', 'tokens', 'condition_id', 'question', 'clobTokenIds']):
                    print("\n=== MARKET ITEM ===")
                    print(json.dumps(item, indent=2)[:1000])
