/* =============================================
   AUTOVAULT SOC DASHBOARD INTERACTIVE JS
   ============================================= */

(function () {
  "use strict";

  // --- Clock ---
  function updateClock() {
    const now = new Date();
    const clockEl = document.getElementById("clock");
    if (clockEl) {
      clockEl.textContent = now.toTimeString().split(" ")[0] + "." + String(now.getMilliseconds()).padStart(3, "0");
    }
  }
  setInterval(updateClock, 50);

  // --- Charts Initialization ---
  const MAX_DATA_POINTS = 30;
  const labels = Array.from({ length: MAX_DATA_POINTS }, (_, i) => `${MAX_DATA_POINTS - i}s ago`);
  const initialEntropyData = Array.from({ length: MAX_DATA_POINTS }, () => 3.0 + Math.random() * 0.8);
  const initialIOData = Array.from({ length: MAX_DATA_POINTS }, () => Math.floor(5 + Math.random() * 10));

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      x: { display: false },
      y: {
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { color: '#7a889b', font: { family: 'JetBrains Mono', size: 10 } }
      }
    },
    plugins: { legend: { display: false } }
  };

  // 1. Entropy Chart
  const ctxEntropy = document.getElementById("entropyChart").getContext("2d");
  const entropyChart = new Chart(ctxEntropy, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Entropy",
          data: initialEntropyData,
          borderColor: "#00ffaa",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.2,
          fill: true,
          backgroundColor: "rgba(0, 255, 170, 0.05)"
        },
        {
          label: "Threshold",
          data: Array(MAX_DATA_POINTS).fill(7.8),
          borderColor: "rgba(255, 51, 102, 0.5)",
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0
        }
      ]
    },
    options: {
      ...chartOptions,
      scales: {
        ...chartOptions.scales,
        y: { ...chartOptions.scales.y, min: 0, max: 8.5 }
      }
    }
  });

  // 2. I/O Velocity Chart
  const ctxIO = document.getElementById("ioChart").getContext("2d");
  const ioChart = new Chart(ctxIO, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "I/O Velocity",
          data: initialIOData,
          borderColor: "#00e5ff",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.2,
          fill: true,
          backgroundColor: "rgba(0, 229, 255, 0.05)"
        },
        {
          label: "Threshold",
          data: Array(MAX_DATA_POINTS).fill(50),
          borderColor: "rgba(255, 51, 102, 0.5)",
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0
        }
      ]
    },
    options: {
      ...chartOptions,
      scales: {
        ...chartOptions.scales,
        y: { ...chartOptions.scales.y, min: 0, max: 300 }
      }
    }
  });

  // --- Terminal Log Helper ---
  const terminal = document.getElementById("terminal");
  const logCountEl = document.getElementById("logCount");
  let eventCounter = 0;

  function appendLog(msg, level = "info") {
    if (!terminal) return;
    const timeStr = new Date().toTimeString().split(" ")[0];
    const div = document.createElement("div");
    div.className = `log-line log-line--${level}`;
    div.innerHTML = `<span class="log-line__ts">[${timeStr}]</span> ${msg}`;
    terminal.appendChild(div);
    terminal.scrollTop = terminal.scrollHeight;
    eventCounter++;
    if (logCountEl) logCountEl.textContent = `${eventCounter} events`;
  }

  document.getElementById("clearLogBtn")?.addEventListener("click", () => {
    if (terminal) terminal.innerHTML = "";
    eventCounter = 0;
    if (logCountEl) logCountEl.textContent = "0 events";
  });

  appendLog("AutoVault Security Operations Center initialized.", "info");
  appendLog("Connecting to local Cyber Agent daemon on ws://localhost:8765...", "info");

  // --- WebSocket Connection ---
  let ws = null;
  let isConnected = false;
  let simInterval = null;

  function connectWS() {
    try {
      ws = new WebSocket("ws://localhost:8765");

      ws.onopen = () => {
        isConnected = true;
        document.getElementById("connDot").className = "dot dot--ok";
        document.getElementById("connLabel").textContent = "AGENT ONLINE";
        appendLog("Connected to Cyber Agent daemon.", "info");
        if (simInterval) clearInterval(simInterval);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleAgentMessage(data);
        } catch (e) {
          console.error("Failed to parse WS msg", e);
        }
      };

      ws.onclose = () => {
        isConnected = false;
        document.getElementById("connDot").className = "dot dot--warn";
        document.getElementById("connLabel").textContent = "SIMULATION MODE";
        appendLog("Disconnected from Agent. Falling back to local simulation mode.", "warn");
        startLocalSimulation();
        setTimeout(connectWS, 3000);
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch (e) {
      startLocalSimulation();
    }
  }

  connectWS();

  // --- UI Update Handler ---
  let peakEntropy = 4.12;

  function updateTelemetryUI(entropy, ioVelocity, churn, threatLevel, anomalyScore, processName = "chrome.exe", pid = 1042) {
    // 1. Update Entropy Chart & Texts
    entropyChart.data.datasets[0].data.shift();
    entropyChart.data.datasets[0].data.push(entropy);
    entropyChart.update();

    if (entropy > peakEntropy) peakEntropy = entropy;
    document.getElementById("entropyTag").textContent = entropy.toFixed(2);
    document.getElementById("entropyCurrent").textContent = entropy.toFixed(2);
    document.getElementById("entropyPeak").textContent = peakEntropy.toFixed(2);
    document.getElementById("entropyStatus").textContent = entropy > 7.8 ? "CRITICAL" : "NORMAL";
    document.getElementById("entropyStatus").className = `metric-row__val metric-row__val--${entropy > 7.8 ? "danger" : "ok"}`;

    // 2. Update I/O Chart & Texts
    ioChart.data.datasets[0].data.shift();
    ioChart.data.datasets[0].data.push(ioVelocity);
    ioChart.update();

    document.getElementById("ioTag").textContent = `${ioVelocity}/s`;
    document.getElementById("ioCurrent").textContent = ioVelocity;
    document.getElementById("ioChurn").textContent = churn;

    // 3. Anomaly Score Fill
    const fillPercent = Math.min(100, Math.max(5, Math.abs(anomalyScore) * 100));
    document.getElementById("scoreFill").style.width = `${fillPercent}%`;
    document.getElementById("scoreNum").textContent = Math.abs(anomalyScore).toFixed(2);

    // 4. Threat Badge
    const badge = document.getElementById("threatBadge");
    const levelEl = document.getElementById("threatLevel");
    badge.setAttribute("data-level", threatLevel);
    levelEl.textContent = threatLevel;

    // 5. Process Table Update
    const procTable = document.getElementById("processTable");
    if (procTable) {
      procTable.innerHTML = `
        <div class="proc-row proc-row--header">
          <span>PID</span><span>PROCESS</span><span>ENTROPY</span><span>RISK</span>
        </div>
        <div class="proc-row ${threatLevel === "CRITICAL" || threatLevel === "HIGH" ? "proc-row--threat" : ""}">
          <span>${pid}</span>
          <span>${processName}</span>
          <span>${entropy.toFixed(2)}</span>
          <span>${threatLevel}</span>
        </div>
        <div class="proc-row">
          <span>894</span>
          <span>svchost.exe</span>
          <span>3.12</span>
          <span>SAFE</span>
        </div>
        <div class="proc-row">
          <span>2140</span>
          <span>python.exe</span>
          <span>3.84</span>
          <span>SAFE</span>
        </div>
      `;
    }
  }

  function handleAgentMessage(data) {
    if (data.type === "telemetry") {
      updateTelemetryUI(data.entropy, data.io_velocity, data.extension_churn, data.threat_level, data.anomaly_score, data.active_process, data.pid);
      if (data.files_scanned) {
        document.getElementById("filesScanned").textContent = data.files_scanned;
      }
    } else if (data.type === "log") {
      appendLog(data.message, data.level ? data.level.toLowerCase() : "info");
    } else if (data.type === "threat") {
      triggerThreatAlert(data.entropy, data.io_velocity, data.process, data.pid);
    } else if (data.type === "lockdown") {
      showLockdownFlash(data.cid, data.tx_hash);
    } else if (data.type === "vault") {
      document.getElementById("vaultCID").textContent = data.cid || "QmVault...";
      document.getElementById("vaultTX").textContent = data.tx_hash || "0x9f3...";
      const countEl = document.getElementById("vaultSnaps");
      if (countEl) countEl.textContent = parseInt(countEl.textContent || "0") + 1;
    }
  }

  // --- Threat Alert & Lockdown Handling ---
  const threatOverlay = document.getElementById("threatOverlay");
  const lockdownFlash = document.getElementById("lockdownFlash");
  let autoLockTimer = null;

  function triggerThreatAlert(entropy, ioVelocity, processName, pid) {
    document.getElementById("alertEntropy").textContent = entropy.toFixed(2);
    document.getElementById("alertIO").textContent = `${ioVelocity}/s`;
    document.getElementById("alertProcess").textContent = processName;
    document.getElementById("alertPID").textContent = pid;

    threatOverlay.removeAttribute("hidden");
    appendLog(`[ALERT] High-entropy process anomaly detected! PID ${pid} (${processName})`, "threat");

    // Auto lockdown countdown
    let left = 10;
    const countEl = document.getElementById("autoLockCountdown");
    const barEl = document.getElementById("autoLockBar");
    barEl.style.width = "100%";

    if (autoLockTimer) clearInterval(autoLockTimer);
    autoLockTimer = setInterval(() => {
      left--;
      if (countEl) countEl.textContent = left;
      barEl.style.width = `${(left / 10) * 100}%`;
      if (left <= 0) {
        clearInterval(autoLockTimer);
        executeLockdownAction();
      }
    }, 1000);
  }

  function executeLockdownAction() {
    if (autoLockTimer) clearInterval(autoLockTimer);
    threatOverlay.setAttribute("hidden", "");

    // Send lockdown to WS agent if connected
    if (isConnected && ws) {
      ws.send(JSON.stringify({ action: "lockdown" }));
    } else {
      // Local fallback simulation lockdown
      const fakeCID = "QmXyZ9876543210" + Math.random().toString(36).substring(2, 8);
      const fakeTX = "0x" + Array.from({length: 40}, () => Math.floor(Math.random()*16).toString(16)).join("");
      showLockdownFlash(fakeCID, fakeTX);
    }
  }

  function showLockdownFlash(cid, tx) {
    document.getElementById("lockdownCID").textContent = cid;
    document.getElementById("lockdownTX").textContent = tx;
    lockdownFlash.removeAttribute("hidden");

    document.getElementById("phaseEnforcer").className = "phase-item phase-item--active";
    document.getElementById("phaseEnforcer").querySelector(".phase-item__status").textContent = "SUSPENDED PID";
    document.getElementById("phaseVault").className = "phase-item phase-item--ok";
    document.getElementById("phaseVault").querySelector(".phase-item__status").textContent = "SNAPSHOTTED";

    appendLog(`[ENFORCER] Malicious process suspended. Network blocked. Clean state backed up to IPFS: ${cid}`, "lockdown");
    appendLog(`[VAULT] Smart Contract triggered on Polygon Amoy. Tx Hash: ${tx}`, "lockdown");

    setTimeout(() => {
      lockdownFlash.setAttribute("hidden", "");
    }, 4000);
  }

  document.getElementById("lockdownBtn")?.addEventListener("click", executeLockdownAction);
  document.getElementById("dismissBtn")?.addEventListener("click", () => {
    if (autoLockTimer) clearInterval(autoLockTimer);
    threatOverlay.setAttribute("hidden", "");
  });

  // --- Buttons Handling ---
  document.getElementById("simAttackBtn")?.addEventListener("click", () => {
    appendLog("Initiating simulated ransomware attack...", "warn");
    if (isConnected && ws) {
      ws.send(JSON.stringify({ action: "simulate_attack" }));
    } else {
      // Local simulation fallback
      triggerThreatAlert(7.94, 284, "ransomware_sim.exe", 4920);
    }
  });

  document.getElementById("resetBtn")?.addEventListener("click", () => {
    appendLog("Resetting security agent & firewall state...", "info");
    peakEntropy = 4.12;
    if (isConnected && ws) {
      ws.send(JSON.stringify({ action: "reset" }));
    }
    document.getElementById("phaseEnforcer").className = "phase-item phase-item--dim";
    document.getElementById("phaseEnforcer").querySelector(".phase-item__status").textContent = "STANDBY";
    document.getElementById("phaseVault").className = "phase-item phase-item--dim";
    document.getElementById("phaseVault").querySelector(".phase-item__status").textContent = "IDLE";
    updateTelemetryUI(3.24, 12, 0, "NORMAL", 0.08);
  });

  document.getElementById("snapshotBtn")?.addEventListener("click", () => {
    appendLog("Creating manual system snapshot...", "info");
    const fakeCID = "QmManualSnap" + Math.random().toString(36).substring(2, 8);
    const fakeTX = "0x" + Array.from({length: 40}, () => Math.floor(Math.random()*16).toString(16)).join("");
    document.getElementById("vaultCID").textContent = fakeCID;
    document.getElementById("vaultTX").textContent = fakeTX;
    const countEl = document.getElementById("vaultSnaps");
    if (countEl) countEl.textContent = parseInt(countEl.textContent || "0") + 1;
    appendLog(`Manual snapshot pinned to IPFS: ${fakeCID}`, "lockdown");
  });

  // --- Local Fallback Telemetry Generator ---
  function startLocalSimulation() {
    if (simInterval) clearInterval(simInterval);
    simInterval = setInterval(() => {
      if (isConnected) return;
      const baseEntropy = 3.0 + Math.random() * 1.2;
      const baseIO = Math.floor(8 + Math.random() * 8);
      updateTelemetryUI(baseEntropy, baseIO, 0, "NORMAL", 0.08);
    }, 1000);
  }

})();
