const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");
require("dotenv").config();

async function main() {
  const networkArg = process.argv[2];
  if (!networkArg || (networkArg !== 'amoy' && networkArg !== 'sepolia')) {
    console.error("Please provide a valid network: 'amoy' or 'sepolia'");
    process.exit(1);
  }

  const networks = {
    amoy: {
      url: "https://rpc-amoy.polygon.technology",
      chainId: 80002,
      name: "Polygon Amoy"
    },
    sepolia: {
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      chainId: 421614,
      name: "Arbitrum Sepolia"
    }
  };

  const network = networks[networkArg];
  
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.error("PRIVATE_KEY not found in .env");
    process.exit(1);
  }

  const provider = new ethers.JsonRpcProvider(network.url);
  const wallet = new ethers.Wallet(privateKey, provider);

  console.log(`Deploying to ${network.name}...`);
  console.log(`Using wallet address: ${wallet.address}`);

  const abi = [
    "constructor(string memory _initialCID)",
    "function triggerEmergencyLockdown() external",
    "function updateCleanCID(string calldata _newCID) external",
    "function restoreSystem() external",
    "function getSnapshotHistory() external view returns (tuple(string cid, uint256 timestamp, string eventType)[] memory)",
    "function getSystemStatus() external view returns (bool, string memory, uint256, uint256)",
    "event LockdownTriggered(string cid, uint256 timestamp, address agent)",
    "event CIDUpdated(string oldCID, string newCID, uint256 timestamp)",
    "event SystemRestored(uint256 timestamp)",
    "error Unauthorized()",
    "error SystemAlreadyCompromised()",
    "error InvalidCID()"
  ];

  // NOTE: Replace this placeholder with the actual compiled bytecode from AutoVaultRecovery.sol
  // You can compile the contract using Hardhat, Foundry, or Remix to get the bytecode.
  const bytecode = "0x"; // PLACEHOLDER_BYTECODE

  if (bytecode === "0x") {
    console.warn("WARNING: Using placeholder bytecode. Contract deployment will fail unless actual bytecode is provided.");
  }

  const factory = new ethers.ContractFactory(abi, bytecode, wallet);
  const initialCID = process.env.INITIAL_CID || "QmInitialCleanState_AutoVault_v1";

  try {
    const contract = await factory.deploy(initialCID);
    console.log("Waiting for deployment transaction...");
    const receipt = await contract.deploymentTransaction().wait();
    const contractAddress = await contract.getAddress();

    console.log("\n✅ Deployment Successful!");
    console.log(`Contract Address: ${contractAddress}`);
    console.log(`Transaction Hash: ${receipt.hash}`);
    
    // DEMO: Use this address in agent/config.py
    
    const status = await contract.getSystemStatus();
    console.log("\n📊 Initial System Status:");
    console.log(`Compromised: ${status[0]}`);
    console.log(`Latest CID: ${status[1]}`);
    console.log(`Snapshots: ${status[2]}`);
    
    const deployInfo = {
      address: contractAddress,
      txHash: receipt.hash,
      chainId: network.chainId,
      deployedAt: new Date().toISOString()
    };
    
    const deploymentsDir = path.join(__dirname, "deployments");
    if (!fs.existsSync(deploymentsDir)) {
      fs.mkdirSync(deploymentsDir);
    }
    
    fs.writeFileSync(
      path.join(deploymentsDir, `${networkArg}.json`),
      JSON.stringify(deployInfo, null, 2)
    );
    
    console.log(`\nDeployment info saved to deployments/${networkArg}.json`);

  } catch (error) {
    console.error("Deployment failed:", error);
  }
}

main();
