import requests
from tabulate import tabulate
import time
from collections import Counter

ETHERSCAN_API_KEY = "6N2TEV35ID3RRXYMJK12762VCMQF6C66SM"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

BLACKLIST = [
    "0x0000000000000000000000000000000000000000",
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  
]

CREATOR_INFO = """
==========================================
  CryptoOSINT by https://t.me/nonstop4ek
  GitHub: https://github.com/MaksKostyuk
==========================================
"""

def get_balance(address):
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params).json()
    if response["status"] == "1":
        balance_eth = int(response["result"]) / 10**18
        return balance_eth
    return None

def get_transactions(address, count=100):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params).json()
    if response["status"] == "1":
        return response["result"][:count]
    return []

def analyze_wallet(address):
    print(CREATOR_INFO)
    print(f"\n🔍 Checking wallet: {address}")

    if is_blacklisted(address, BLACKLIST):
        print("⚠️ Warning: This wallet is blacklisted!")

    balance = get_balance(address)
    if balance is not None:
        print(f"💰 Balance: {balance:.5f} ETH")
        eth_usd = get_eth_usd_price()
        if eth_usd:
            print(f"💵 Approximate USD value: ${balance * eth_usd:.2f}")
    else:
        print("⚠️ Failed to fetch balance.")

    txs = get_transactions(address)
    if txs:
        print(f"\n📜 Last {len(txs)} transactions:")
        table = []
        for tx in txs:
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx['timeStamp'])))
            value_eth = int(tx['value']) / 10**18
            table.append([ts, tx['from'], tx['to'], f"{value_eth:.5f}"])
        print(tabulate(table, headers=["Timestamp", "From", "To", "ETH Value"]))
        print(f"\n📊 Transactions last month: {count_transactions_last_month(address, txs)}")
        print(f"🤝 Top counterparties:")
        for addr, cnt in analyze_counterparties(txs):
            print(f" - {addr} : {cnt} txs")
    else:
        print("⚠️ No transactions found or wallet is empty.")

    print("\n🎨 NFTs owned:")
    nfts = get_nfts(address)
    if nfts:
        for name, collection in nfts:
            print(f" - {name} from {collection}")
    else:
        print(" No NFTs found.")

    ens = get_ens_name(address)
    if ens:
        print(f"\n🌐 ENS Name: {ens}")
    else:
        print("\n🌐 ENS Name: Not found")

    tokens = get_token_balances(address)
    if tokens:
        print("\n🔗 ERC-20 Tokens:")
        for sym, bal in tokens:
            print(f" - {sym}: {bal:.5f}")
    else:
        print("\n🔗 No ERC-20 tokens found or API limit reached.")

def is_blacklisted(address, blacklist):
    return address.lower() in (a.lower() for a in blacklist)

def count_transactions_last_month(address, txs):
    now = int(time.time())
    one_month_ago = now - 30*24*60*60
    recent_txs = [tx for tx in txs if int(tx['timeStamp']) >= one_month_ago]
    return len(recent_txs)

def analyze_counterparties(txs, top_n=5):
    addresses = [tx['to'].lower() for tx in txs] + [tx['from'].lower() for tx in txs]
    counter = Counter(addresses)
    return counter.most_common(top_n)

def get_eth_usd_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ethereum", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("ethereum", {}).get("usd", None)
    return None

def get_ens_name(address):
    params = {
        "module": "account",
        "action": "getens",
        "address": address,
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params).json()
    if response["status"] == "1" and response["result"]:
        return response["result"]
    return None

def get_nfts(address):
    url = "https://api.opensea.io/api/v1/assets"
    params = {
        "owner": address,
        "order_direction": "desc",
        "limit": 10,
        "offset": 0
    }
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        assets = response.json().get("assets", [])
        return [(asset.get("name", "Unnamed"), asset.get("collection", {}).get("name", "Unknown")) for asset in assets]
    return []

def get_token_balances(address):
    url = f"https://api.ethplorer.io/getAddressInfo/{address}"
    params = {"apiKey": "freekey"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        tokens = data.get("tokens", [])
        result = []
        for token in tokens:
            info = token.get("tokenInfo", {})
            decimals = int(info.get("decimals", 0)) if info.get("decimals") else 0
            balance = float(token.get("balance", 0)) / (10 ** decimals if decimals else 1)
            symbol = info.get("symbol", "UNKNOWN")
            result.append((symbol, balance))
        return result
    return []

if __name__ == "__main__":
    while True:
        eth_address = input("Enter ETH address (or 'exit' to quit): ").strip()
        if eth_address.lower() == "exit":
            print("Goodbye!")
            break
        analyze_wallet(eth_address)
        print("\n---\n")
