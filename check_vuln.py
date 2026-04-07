from web3 import Web3

# เชื่อมต่อกับ Ethereum Node (ใช้ Public RPC ที่เสถียร)
W3RPC = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(W3RPC))

def huntvulnerability(address):
    if not w3.is_address(address):
        return "❌ Address ไม่กริปวะพี่ เช็คด่วน!"

    # ดึง Bytecode ออกมาดูโครงสร้าง
    bytecode = w3.eth.get_code(address).hex()

    if bytecode == "0x" or bytecode == "":
        return "⚠️ นี่มัน Wallet ธรรมดาพี่ ไม่มีโค้ดให้ AI จัด!"

    print(f"\n--- Target Address: {address} ---")
    print(f"Bytecode Length: {len(bytecode)} characters")

    # Logic สแกนหาจุดตาย (Reentrancy pattern / Delegatecall)
    vulnerabilities = []
    if "f3" in bytecode and "55" in bytecode:
        vulnerabilities.append("[!] สัญญาณ Re-entry: มีความเสี่ยงในการถูกดึงเหรียญซ้ำ!")
    if "f1" in bytecode:
        vulnerabilities.append("[!] สัญญาณ Call: พบพฤติกรรมการส่งค่าออกภายนอก!")

    if vulnerabilities:
        return "\n".join(vulnerabilities)
    return "✅ เบื้องต้นยังไม่เจอจุดอ่อนที่ชัดเจนพี่!"

if __name__ == "__main__":
    target = input("ใส่ Address เป้าหมายมาสิไก่อะไร: ").strip()
    print(huntvulnerability(target))

