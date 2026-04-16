from dotenv import load_dotenv
load_dotenv()
import os
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, BalanceAllowanceParams, AssetType

creds = ApiCreds(
    api_key=os.getenv('POLYMARKET_API_KEY'),
    api_secret=os.getenv('POLYMARKET_API_SECRET'),
    api_passphrase=os.getenv('POLYMARKET_API_PASSPHRASE')
)

print(f'Using funder: {os.getenv("POLYMARKET_FUNDER")}')

client = ClobClient(
    host='https://clob.polymarket.com',
    chain_id=137,
    key=os.getenv('POLYMARKET_PRIVATE_KEY'),
    creds=creds,
    funder=os.getenv('POLYMARKET_FUNDER'),
    signature_type=1 if os.getenv('POLYMARKET_FUNDER') else 0
)

resp = client.get_balance_allowance(BalanceAllowanceParams(asset_type=AssetType.COLLATERAL))
print(f'Full response: {resp}')
print(f'Balance: {resp.get("balance", "N/A")}')
