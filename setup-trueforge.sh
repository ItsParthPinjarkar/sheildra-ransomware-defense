#!/bin/bash
# AutoVault + TrueForge Setup Script
# This script sets up the TrueForge agent harness integration

set -e

echo "=========================================="
echo "  AutoVault + TrueForge Setup"
echo "=========================================="
echo ""

# Check Node.js version
echo "Checking Node.js version..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "Error: TrueForge requires Node.js 22 or newer"
    echo "Current version: $(node -v)"
    echo "Please upgrade Node.js: https://nodejs.org/"
    exit 1
fi
echo "✓ Node.js $(node -v) detected"

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
cd agent
pip install -r requirements.txt
pip install mcp  # MCP package for the server
cd ..

# Install Node.js dependencies
echo ""
echo "Installing Node.js dependencies..."
npm install

# Create test vault directory
echo ""
echo "Creating test vault directory..."
mkdir -p test_vault

# Generate sample files
echo "Generating sample files for testing..."
python3 -c "
import os
import datetime

test_vault = './test_vault'
os.makedirs(test_vault, exist_ok=True)

files = [
    'README.txt', 'document.docx', 'report.pdf',
    'config.json', 'keys.txt', 'database.sql',
    'backup.zip', 'invoice.xlsx', 'photo.jpg', 'source.py'
]

for filename in files:
    filepath = os.path.join(test_vault, filename)
    with open(filepath, 'w') as f:
        f.write(f'Sample content for {filename}\n')
        f.write(f'Generated at {datetime.datetime.now().isoformat()}\n')
        f.write(f'This is a test file for AutoVault monitoring.\n')
"

echo "✓ Test vault created with sample files"

# Create environment file
echo ""
echo "Creating environment configuration..."
if [ ! -f .env ]; then
    cat > .env << 'EOF'
# AutoVault + TrueForge Configuration

# Watch folder for monitoring
WATCH_FOLDER=./test_vault

# ML Thresholds
ENTROPY_THRESHOLD=7.8
IO_VELOCITY_THRESHOLD=50

# WebSocket Server
WS_HOST=localhost
WS_PORT=8765

# Pinata IPFS (optional)
PINATA_API_KEY=
PINATA_SECRET=

# Blockchain (Polygon Amoy)
RPC_URL=https://rpc-amoy.polygon.technology
CONTRACT_ADDRESS=
PRIVATE_KEY=

# Demo Mode (set to false for real blockchain)
DEMO_MODE=True

# TrueForge Configuration
TRUEFORGE_PORT=8790
TRUEFORGE_MODEL=gpt-4o
EOF
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start TrueForge agent harness:"
echo "   npx @truefoundry/trueforge"
echo ""
echo "2. Open TrueForge UI:"
echo "   http://localhost:8790"
echo ""
echo "3. Configure the agent in TrueForge:"
echo "   - Import: trueforge-agent.yaml"
echo "   - Add MCP server: autovault-mcp"
echo "   - Enable sandbox: daytona"
echo "   - Set up approval checkpoints"
echo ""
echo "4. Start AutoVault agent:"
echo "   cd agent && python main.py"
echo ""
echo "5. Open dashboard:"
echo "   open dashboard/index.html"
echo ""
echo "6. Test the integration:"
echo "   - Click 'Simulate Attack' in dashboard"
echo "   - Watch TrueForge agent respond"
echo "   - Approve lockdown when prompted"
echo ""
echo "Happy hacking! 🚀"
