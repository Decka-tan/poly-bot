import requests
import re
import json

url = "https://polymarket.com/event/btc-updown-5m-1776357600"
resp = requests.get(url)
html = resp.text

# Extract __NEXT_DATA__
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
data = json.loads(next_data_match.group(1))

# Save full data buat inspect
with open('next_data.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Saved to next_data.json")

# Cari semua yang ada "token" atau "condition"
def find_tokens(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}" if path else k
            if 'token' in k.lower() or 'condition' in k.lower():
                print(f"{new_path}: {v}")
            find_tokens(v, new_path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_tokens(v, f"{path}[{i}]")

print("\n=== Searching for tokens/conditions ===")
find_tokens(data)

# Cari market data di dehydratedState
dehydrated = data.get('props', {}).get('pageProps', {})
print(f"\n=== pageProps keys ===")
for k in dehydrated.keys():
    v = dehydrated[k]
    if isinstance(v, (dict, list)):
        print(f"{k}: {type(v).__name__} with {len(v) if isinstance(v, (dict, list)) else '?'} items")
    else:
        print(f"{k}: {v}")
