# 🛡️ AutoVault — AI-Powered Ransomware Defense System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Solidity](https://img.shields.io/badge/Solidity-0.8.20-lightgrey)
![Polygon](https://img.shields.io/badge/Network-Polygon_Amoy-purple)
![IPFS](https://img.shields.io/badge/Storage-IPFS-teal)

AutoVault is a next-generation ransomware defense mechanism that combines on-device machine learning with decentralized storage and blockchain immutability to detect, stop, and recover from ransomware attacks in real-time.

---

## 🏗️ Architecture

```text
+-------------------+       +-------------------+       +-------------------+
|    Watchdog       |       |       Brain       |       |    Enforcer       |
| (File Monitoring) | ----> |   (ML Detection)  | ----> | (Action/Lockdown) |
+-------------------+       +-------------------+       +-------------------+
                                                              |
                                                              v
                                                    +-------------------+
                                                    |      Vault        |
                                                    | (IPFS & Contract) |
                                                    +-------------------+
```

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Agent Core** | Python 3.10+ | Orchestrates system monitoring and defense |
| **ML Engine** | scikit-learn | Detects anomalous file operations |
| **Messaging** | websockets | Real-time communication with the dashboard |
| **Blockchain Sync** | Web3.py | Interacts with smart contracts |
| **Smart Contract** | Solidity 0.8.20 | Immutable audit trail and lockdown state |
| **Networks** | Polygon Amoy | Fast, low-cost L2 for contract deployment |
| **Storage** | IPFS / Pinata | Decentralized, tamper-proof file snapshots |
| **UI** | Chart.js | Visualizes system health and attack metrics |
| **Deployment** | ethers.js | JavaScript deployment scripting |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Setup the Agent
```bash
cd agent
pip install -r requirements.txt
```

### 2. Run the Agent
```bash
python main.py
```

### 3. Open the Dashboard
Open `dashboard/index.html` in your favorite web browser.

### 4. Demo an Attack
Click **Simulate Ransomware Attack** in the dashboard, OR run:
```bash
python ransim.py
```

---

## 🔗 Smart Contract Deployment

Deploy the AutoVault smart contract to maintain an immutable record of system state.

1. Navigate to the contracts directory:
```bash
cd contracts
npm install
```

2. Configure your environment:
- Copy `.env.example` to `.env`
- Add your `PRIVATE_KEY`

3. Deploy to Polygon Amoy:
*(Ensure you have testnet MATIC from an Amoy faucet)*
```bash
npm run deploy:amoy
```

4. Configure the Agent:
- Copy the deployed contract address.
- Paste it into `agent/config.py` under `CONTRACT_ADDRESS`.

---

## ⚙️ How It Works

1. **Watchdog Phase**: Monitors file system activity, entropy changes, and high-frequency modifications in designated directories.
2. **Brain Phase**: Analyzes the metrics using an isolation forest ML model to detect patterns indicative of ransomware (e.g., rapid encryption).
3. **Enforcer Phase**: If an attack is detected, the Enforcer immediately kills suspicious processes and isolates the affected directories.
4. **Vault Phase**: Triggers a smart contract transaction to log the lockdown state and retrieves the last known clean snapshot from IPFS to restore files.

---

## 🎬 Demo Flow

Here is what happens during a typical 60-second demo:
1. **Normal Operation**: The agent monitors files, taking periodic IPFS snapshots and updating the smart contract.
2. **Attack Simulation**: The attacker script (`ransim.py`) begins rapidly "encrypting" files.
3. **Detection**: The ML model spikes in anomaly score.
4. **Lockdown**: The agent terminates the attack process, locks the directories, and sends a lockdown transaction to the blockchain.
5. **Recovery**: The agent pulls the latest clean CID from the smart contract, fetches it from IPFS, and restores the original files.

---

## 🔧 Configuration

All configurations can be found in `config.py`.

- `MONITOR_DIR`: The directory path to monitor.
- `ANOMALY_THRESHOLD`: The ML confidence score required to trigger a lockdown.
- `IPFS_ENDPOINT`: Your IPFS node or pinning service API URL.
- `CONTRACT_ADDRESS`: The deployed Solidity contract address.
- `RPC_URL`: The RPC endpoint for the blockchain network.

---

## 🏆 Hackathon Notes

- **Simulated**: The ML model in the demo uses simplified features for reliable demonstration. The ransomware simulator performs benign file modifications rather than actual encryption.
- **Real**: The blockchain transactions, IPFS pinning, websocket dashboard, and process termination logic are all fully functional.

---

## 📄 License

MIT License
