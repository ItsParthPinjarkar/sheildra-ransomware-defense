// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AutoVaultRecovery
 * @dev Smart contract for AI-Powered Ransomware Defense System
 */
contract AutoVaultRecovery {
    string public latestCleanCID;
    address public authorizedAgent;
    bool public isCompromised;
    uint256 public snapshotCount;
    uint256 public lastSnapshotTime;

    struct SnapshotRecord {
        string cid;
        uint256 timestamp;
        string eventType;
    }

    SnapshotRecord[] public snapshotHistory;

    event LockdownTriggered(string cid, uint256 timestamp, address agent);
    event CIDUpdated(string oldCID, string newCID, uint256 timestamp);
    event SystemRestored(uint256 timestamp);

    error Unauthorized();
    error SystemAlreadyCompromised();
    error InvalidCID();

    modifier onlyAgent() {
        if (msg.sender != authorizedAgent) revert Unauthorized();
        _;
    }

    /**
     * @dev Constructor to initialize the contract with an initial clean CID.
     * @param _initialCID The initial IPFS CID of the clean state.
     */
    constructor(string memory _initialCID) {
        latestCleanCID = _initialCID;
        authorizedAgent = msg.sender;
    }

    /**
     * @dev Triggers an emergency lockdown of the system.
     */
    function triggerEmergencyLockdown() external onlyAgent {
        if (isCompromised) revert SystemAlreadyCompromised();
        isCompromised = true;
        snapshotHistory.push(SnapshotRecord({
            cid: latestCleanCID,
            timestamp: block.timestamp,
            eventType: "LOCKDOWN"
        }));
        emit LockdownTriggered(latestCleanCID, block.timestamp, msg.sender);
    }

    /**
     * @dev Updates the clean CID of the system.
     * @param _newCID The new IPFS CID to update to.
     */
    function updateCleanCID(string calldata _newCID) external onlyAgent {
        if (bytes(_newCID).length == 0) revert InvalidCID();
        string memory oldCID = latestCleanCID;
        latestCleanCID = _newCID;
        snapshotCount++;
        lastSnapshotTime = block.timestamp;
        
        snapshotHistory.push(SnapshotRecord({
            cid: _newCID,
            timestamp: block.timestamp,
            eventType: "UPDATE"
        }));

        emit CIDUpdated(oldCID, _newCID, block.timestamp);
    }

    /**
     * @dev Restores the system to a clean state.
     */
    function restoreSystem() external onlyAgent {
        isCompromised = false;
        snapshotHistory.push(SnapshotRecord({
            cid: latestCleanCID,
            timestamp: block.timestamp,
            eventType: "RESTORE"
        }));
        emit SystemRestored(block.timestamp);
    }

    /**
     * @dev Returns the full history of snapshots.
     * @return SnapshotRecord[] Array of all snapshot records.
     */
    function getSnapshotHistory() external view returns (SnapshotRecord[] memory) {
        return snapshotHistory;
    }

    /**
     * @dev Returns the current status of the system.
     * @return isCompromised Boolean indicating if the system is compromised.
     * @return latestCleanCID The latest clean IPFS CID.
     * @return snapshotCount The total number of snapshots taken.
     * @return lastSnapshotTime The timestamp of the last snapshot.
     */
    function getSystemStatus() external view returns (bool, string memory, uint256, uint256) {
        return (isCompromised, latestCleanCID, snapshotCount, lastSnapshotTime);
    }
}
