import asyncio
import websockets
import json
import time
import os
import traceback
import config
from brain import ThreatBrain
from watchdog_monitor import FileWatcher
from vault import BlockchainVault
from enforcer import execute_lockdown, restore_network
import ransim

class AutoVaultAgent:
    def __init__(self):
        self.brain = ThreatBrain()
        self.watcher = FileWatcher(config.WATCH_FOLDER)
        self.vault = BlockchainVault()
        self.lockdown_active = False
        self.lockdown_timer = 0
        self.connected_clients = set()

    async def broadcast(self, message: dict):
        if self.connected_clients:
            msg_str = json.dumps(message)
            await asyncio.gather(*[client.send(msg_str) for client in self.connected_clients], return_exceptions=True)

    async def log(self, message: str, level="INFO"):
        print(f"[{level}] {message}")
        await self.broadcast({
            "type": "log",
            "ts": time.time(),
            "level": level,
            "message": message
        })

    async def handle_client(self, websocket):
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    action = data.get("action")
                    if action == "simulate_attack":
                        await self.log("Starting ransomware simulation...")
                        ransim.simulate_ransomware(config.WATCH_FOLDER)
                    elif action == "reset":
                        await self.log("Resetting environment...")
                        restore_network()
                        self.lockdown_active = False
                        self.watcher.current_extension_churn = 0
                        ransim.setup_test_vault(config.WATCH_FOLDER)
                        await self.log("Environment reset complete.")
                except json.JSONDecodeError:
                    pass
        finally:
            self.connected_clients.remove(websocket)

    async def main_loop(self):
        self.watcher.start()
        await self.log("AutoVault Agent Started. Monitoring active.")
        
        while True:
            now = time.time()
            
            # Reset lockdown timer
            if self.lockdown_active and now > self.lockdown_timer:
                self.lockdown_active = False
                await self.log("Lockdown cooldown expired.")
                
            telemetry = self.watcher.get_telemetry()
            analysis = self.brain.analyze(
                telemetry['entropy'],
                telemetry['io_velocity'],
                telemetry['extension_churn']
            )
            
            # Broadcast telemetry
            await self.broadcast({
                "type": "telemetry",
                "ts": now,
                "entropy": telemetry['entropy'],
                "io_velocity": telemetry['io_velocity'],
                "extension_churn": telemetry['extension_churn'],
                "anomaly_score": analysis['anomaly_score'],
                "is_threat": analysis['is_threat'],
                "threat_level": analysis['threat_level'],
                "active_process": telemetry['active_process'],
                "pid": telemetry['pid'],
                "files_scanned": telemetry['files_scanned']
            })
            
            if analysis['is_threat'] and not self.lockdown_active:
                await self.log("THREAT DETECTED! Initiating lockdown...", "CRITICAL")
                
                await self.broadcast({
                    "type": "threat",
                    "ts": now,
                    "entropy": telemetry['entropy'],
                    "io_velocity": telemetry['io_velocity'],
                    "process": telemetry['active_process'],
                    "pid": telemetry['pid']
                })
                
                # Snapshot
                cid = self.vault.take_snapshot(config.WATCH_FOLDER)
                
                # Lockdown
                lockdown_result = execute_lockdown(telemetry['pid'], cid)
                
                await self.broadcast({
                    "type": "lockdown",
                    "ts": now,
                    "pid": telemetry['pid'],
                    "suspended": lockdown_result['suspended'],
                    "network_blocked": lockdown_result['network_blocked'],
                    "cid": cid,
                    "tx_hash": "" # to be updated
                })
                
                # Blockchain
                tx_hash = self.vault.trigger_lockdown_contract(cid)
                vault_status = self.vault.get_status()
                
                await self.broadcast({
                    "type": "vault",
                    "ts": now,
                    "cid": cid,
                    "tx_hash": tx_hash,
                    "block_number": vault_status['block_number']
                })
                
                self.lockdown_active = True
                self.lockdown_timer = now + 20.0
                await self.log(f"Lockdown complete. CID: {cid}, TX: {tx_hash}")

            await asyncio.sleep(0.5)

async def main():
    print("========================================")
    print("         AutoVault Agent v1.0           ")
    print("========================================")
    
    # Setup test vault
    ransim.setup_test_vault(config.WATCH_FOLDER)
    ransim.simulate_normal_activity(config.WATCH_FOLDER)
    
    agent = AutoVaultAgent()
    
    server = await websockets.serve(agent.handle_client, config.WS_HOST, config.WS_PORT)
    print(f"WebSocket server listening on ws://{config.WS_HOST}:{config.WS_PORT}")
    
    try:
        await agent.main_loop()
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        agent.watcher.stop()
        restore_network()
        server.close()
        await server.wait_closed()
        print("AutoVault Agent shutdown gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
