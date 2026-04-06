from flask import Flask, render_template
import requests
import config

app = Flask(__name__)

def get_eth_price():
    try:
        res = requests.get(config.COINGECKO_URL, timeout=5)
        data = res.json()
        return data['ethereum']['usd']
    except:
        return 2000.0

def get_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        res = requests.post(config.RPC_URL, json=payload, timeout=5)
        result = res.json()
        if 'result' in result:
            balance_wei = int(result['result'], 16)
            return balance_wei / 1e18
        else:
            return 0.0
    except:
        return 0.0
@app.route('/')
def index():
    whale_data = []
    eth_price = get_eth_price()
    
    for whale in config.WHALES:
        bal_eth = get_balance(whale['address'])
        bal_usd = bal_eth * eth_price
        whale_data.append({
            "name": whale['name'],
            "address": whale['address'],
            "balance_eth": f"{bal_eth:.4f}",
            "balance_usd": f"${bal_usd:,.2f}"
        })
    
    return render_template('index.html', whales=whale_data, eth_price=f"${eth_price:,.2f}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
