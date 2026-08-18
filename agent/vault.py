import os
import hashlib
import json
import requests
from web3 import Web3
import config

# Inline ABI
AUTOVAULT_ABI = """
[
    {
        "inputs": [],
        "name": "triggerEmergencyLockdown",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "cid",
                "type": "string"
            }
        ],
        "name": "updateCleanCID",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
"""

class BlockchainVault:
    def __init__(self):
        self.demo_mode = config.DEMO_MODE
        self.connected = False
        self.latest_cid = ""
        self.latest_tx = ""
        self.block_number = 0
        
        if not self.demo_mode:
            try:
                self.w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
                self.connected = self.w3.is_connected()
                if self.connected:
                    self.block_number = self.w3.eth.block_number
                    self.contract = self.w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=json.loads(AUTOVAULT_ABI))
            except Exception:
                self.connected = False
        else:
            self.connected = True
            
    def take_snapshot(self, folder_path):
        if self.demo_mode:
            h = hashlib.sha256()
            try:
                for entry in os.scandir(folder_path):
                    if entry.is_file():
                        with open(entry.path, 'rb') as f:
                            h.update(f.read())
            except Exception:
                pass
            cid = f"QmDemo{h.hexdigest()[:20]}"
            self.latest_cid = cid
            return cid
        else:
            if not config.PINATA_API_KEY or not config.PINATA_SECRET:
                return "QmFakeCIDNoCreds"
            headers = {
                'pinata_api_key': config.PINATA_API_KEY,
                'pinata_secret_api_key': config.PINATA_SECRET
            }
            try:
                response = requests.post("https://api.pinata.cloud/pinning/pinJSONToIPFS", json={"snapshot": "test"}, headers=headers)
                if response.status_code == 200:
                    cid = response.json().get('IpfsHash')
                    self.latest_cid = cid
                    return cid
            except Exception:
                pass
            return "QmErrorCID"
            
    def trigger_lockdown_contract(self, cid):
        if self.demo_mode:
            tx_hash = "0x" + os.urandom(32).hex()
            self.latest_tx = tx_hash
            self.block_number += 1
            return tx_hash
        else:
            if not self.connected or not config.PRIVATE_KEY:
                return "0xErrorTx"
            try:
                account = self.w3.eth.account.from_key(config.PRIVATE_KEY)
                nonce = self.w3.eth.get_transaction_count(account.address)
                tx1 = self.contract.functions.triggerEmergencyLockdown().build_transaction({
                    'chainId': self.w3.eth.chain_id,
                    'gas': 2000000,
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': nonce,
                })
                signed_tx1 = self.w3.eth.account.sign_transaction(tx1, private_key=config.PRIVATE_KEY)
                tx_hash1 = self.w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
                
                nonce += 1
                tx2 = self.contract.functions.updateCleanCID(cid).build_transaction({
                    'chainId': self.w3.eth.chain_id,
                    'gas': 2000000,
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': nonce,
                })
                signed_tx2 = self.w3.eth.account.sign_transaction(tx2, private_key=config.PRIVATE_KEY)
                tx_hash2 = self.w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
                
                self.latest_tx = self.w3.to_hex(tx_hash2)
                return self.latest_tx
            except Exception as e:
                return f"0xErrorTx: {str(e)}"

    def get_status(self):
        return {
            'connected': self.connected,
            'latest_cid': self.latest_cid,
            'latest_tx': self.latest_tx,
            'block_number': self.block_number,
            'demo_mode': self.demo_mode
        }
