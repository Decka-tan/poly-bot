import requests
import re
import json

# Fetch langsung dari Polymarket website
url = "https://polymarket.com/event/btc-updown-5m-1776357600"

resp = requests.get(url)
html = resp.text

# Cari token IDs (pattern: 0x... alphanumeric 42 chars)
tokens = re.findall(r'0x[a-fA-F0-9]{40}', html)
print(f"Found {len(tokens)} potential addresses/tokens")

# Cari price data
prices = re.findall(r'"price":\s*([0-9.]+)', html)
print(f"Found {len(prices)} prices")

# Cari condition ID
conditions = re.findall(r'"condition_id":\s*"([^"]+)"', html)
print(f"Found {len(conditions)} condition IDs")
for c in conditions[:5]:
    print(f"  - {c}")

# Cari market data di script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for script in scripts:
    if 'token_id' in script and len(script) < 10000:  # reasonable size
        # Coba parse JSON
        try:
            # Extract JSON-like structures
            jsons = re.findall(r'\{[^{}]*"[^"]*token[^"]*"[^{}]*\}', script)
            for j in jsons[:3]:
                print(f"\nJSON fragment: {j[:200]}...")
        except:
            pass
