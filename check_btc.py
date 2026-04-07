import requests
import sys

def check_address(address):
    url = f"https://mempool.space/api/address/{address}"
    try:
        r = requests.get(url)
        data = r.json()
        
        tx_count = data['chain_stats']['tx_count']
        balance = data['chain_stats']['balance'] / 100000000
        
        print(f"Address: {address}")
        print(f"Balance: {balance} BTC")
        print(f"Total Transactions: {tx_count}")
        
        if tx_count > 1:
            print("⚠️ WARNING: Address Reuse Detected! (Privacy Risk)")
        else:
            print("✅ Good: No Address Reuse detected.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # เปลี่ยน Address ด้านล่างเป็น Address ที่ต้องการเช็ค
    target = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" 
    check_address(target)

