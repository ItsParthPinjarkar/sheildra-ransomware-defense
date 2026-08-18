import os

WATCH_FOLDER = os.environ.get("WATCH_FOLDER", "./test_vault")
ENTROPY_THRESHOLD = float(os.environ.get("ENTROPY_THRESHOLD", 7.8))
IO_VELOCITY_THRESHOLD = int(os.environ.get("IO_VELOCITY_THRESHOLD", 50))
WS_HOST = os.environ.get("WS_HOST", "localhost")
WS_PORT = int(os.environ.get("WS_PORT", 8765))
PINATA_API_KEY = os.environ.get("PINATA_API_KEY", "")
PINATA_SECRET = os.environ.get("PINATA_SECRET", "")
RPC_URL = os.environ.get("RPC_URL", "https://rpc-amoy.polygon.technology")
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", "")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "")
DEMO_MODE = os.environ.get("DEMO_MODE", "True").lower() in ("true", "1", "yes")
