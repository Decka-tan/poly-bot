from dotenv import load_dotenv
load_dotenv()
import os
from eth_account import Account
import requests

addr = Account.from_key(os.getenv('POLYMARKET_PRIVATE_KEY')).address
print(f'FUNDER: {os.getenv("POLYMARKET_FUNDER", "none")}')
print(f'Signer: {addr}')

# Pakai FUNDER kalau ada
check_addr = os.getenv('POLYMARKET_FUNDER') or addr
print(f'Checking: {check_addr}')

resp = requests.get(f'https://data-api.polymarket.com/wallet?address={check_addr}')
print(f'Status: {resp.status_code}')
print(f'Response: {resp.text}')
