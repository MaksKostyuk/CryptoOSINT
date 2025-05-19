# CryptoOSINT — Ethereum Wallet Analysis Tool

A tool for gathering and analyzing information about Ethereum wallets, including balance, transactions, tokens, NFTs, and ENS names.

---

## Description

This script fetches data about an Ethereum wallet using public APIs (Etherscan, OpenSea, Ethplorer, CoinGecko).  
It displays the ETH balance, approximate USD value, recent transactions, activity analysis, top counterparties, owned NFTs, ERC-20 tokens, and ENS name.

---

## Features

- Check wallet balance
- Display recent transactions (default 100)
- Count transactions in the last month
- Identify top counterparties by transaction count
- Retrieve NFTs owned via OpenSea API
- Show ERC-20 tokens
- Look up ENS (Ethereum Name Service) names
- Check against a blacklist of addresses

---

## Requirements

- Python 3.7+
- Libraries:  
  `requests`  
  `tabulate`

Install dependencies with:

```bash
pip install requests tabulate
