/* =============================================
   main.js — Integrated AutoVault Single Page Application
   ============================================= */

(function () {
  "use strict";

  /* -----------------------------------------------
     1. FULL-WEBPAGE VIEW SWITCHER
  ----------------------------------------------- */
  const navLinks = document.querySelectorAll(".nav-pill__link, .mobile-menu__link");
  const views = document.querySelectorAll(".page-view");

  function switchView(viewId) {
    navLinks.forEach((link) => {
      if (link.dataset.view === viewId) {
        link.classList.add("is-active");
        link.setAttribute("aria-current", "page");
      } else {
        link.classList.remove("is-active");
        link.removeAttribute("aria-current");
      }
    });

    views.forEach((view) => {
      if (view.id === `view-${viewId}`) {
        view.classList.add("is-active");
      } else {
        view.classList.remove("is-active");
      }
    });

    if (viewId === "soc") {
      initSOCCharts();
    }
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      switchView(link.dataset.view);
      closeMobileMenu();
    });
  });

  // Hero buttons
  document.getElementById("heroConsoleBtn")?.addEventListener("click", () => switchView("soc"));
  document.getElementById("heroSandboxBtn")?.addEventListener("click", () => switchView("sandbox"));
  document.getElementById("navDeployBtn")?.addEventListener("click", () => switchView("soc"));
  document.getElementById("mobileDeployBtn")?.addEventListener("click", () => {
    closeMobileMenu();
    switchView("soc");
  });
  document.getElementById("logoBtn")?.addEventListener("click", (e) => {
    e.preventDefault();
    switchView("home");
  });

  /* -----------------------------------------------
     2. MOBILE MENU LOGIC
  ----------------------------------------------- */
  const burgerBtn = document.getElementById("burgerBtn");
  const mobileMenu = document.getElementById("mobileMenu");
  const menuOverlay = document.getElementById("menuOverlay");
  let isMenuOpen = false;

  function openMobileMenu() {
    isMenuOpen = true;
    burgerBtn.classList.add("is-open");
    mobileMenu.removeAttribute("hidden");
    menuOverlay.classList.add("is-visible");
    document.body.classList.add("menu-open");
  }

  function closeMobileMenu() {
    isMenuOpen = false;
    burgerBtn.classList.remove("is-open");
    mobileMenu.setAttribute("hidden", "");
    menuOverlay.classList.remove("is-visible");
    document.body.classList.remove("menu-open");
  }

  burgerBtn?.addEventListener("click", () => {
    isMenuOpen ? closeMobileMenu() : openMobileMenu();
  });

  menuOverlay?.addEventListener("click", closeMobileMenu);

  /* -----------------------------------------------
     3. COUNT-UP STATS
  ----------------------------------------------- */
  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function animateCount(el, target, suffix, decimals, duration) {
    const start = performance.now();
    function frame(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      const current = eased * target;
      el.textContent = current.toFixed(decimals) + suffix;

      if (progress < 1) {
        requestAnimationFrame(frame);
      } else {
        el.textContent = target.toFixed(decimals) + suffix;
      }
    }
    requestAnimationFrame(frame);
  }

  const statValues = document.querySelectorAll(".stat__value");
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (prefersReduced) {
    statValues.forEach((el) => {
      const target = parseFloat(el.dataset.target);
      const suffix = el.dataset.suffix || "";
      const decimals = parseInt(el.dataset.decimals, 10) || 0;
      el.textContent = target.toFixed(decimals) + suffix;
    });
  } else {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseFloat(el.dataset.target);
            const suffix = el.dataset.suffix || "";
            const decimals = parseInt(el.dataset.decimals, 10) || 0;
            const duration = parseInt(el.dataset.duration, 10) || 1500;
            const delay = parseInt(el.dataset.delay, 10) || 0;

            setTimeout(() => {
              animateCount(el, target, suffix, decimals, duration);
            }, delay);

            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.25 }
    );

    statValues.forEach((el) => observer.observe(el));
  }

  /* -----------------------------------------------
     4. SOC REAL-TIME CHARTS & WEBSOCKET ENGINE
  ----------------------------------------------- */
  let entropyChart = null;
  let ioChart = null;
  let isChartInitialized = false;

  function initSOCCharts() {
    if (isChartInitialized) return;
    isChartInitialized = true;

    const MAX_POINTS = 25;
    const dummyLabels = Array.from({ length: MAX_POINTS }, (_, i) => `${MAX_POINTS - i}s ago`);
    const initialEntropy = Array.from({ length: MAX_POINTS }, () => 3.0 + Math.random() * 0.8);
    const initialIO = Array.from({ length: MAX_POINTS }, () => Math.floor(5 + Math.random() * 8));

    const chartOpts = {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: { display: false },
        y: {
          grid: { color: "rgba(15, 23, 42, 0.12)" },
          ticks: { color: "#0f172a", font: { family: "JetBrains Mono", size: 11, weight: "700" } }
        }
      },
      plugins: { legend: { display: false } }
    };

    const ctxE = document.getElementById("entropyCanvas")?.getContext("2d");
    if (ctxE) {
      entropyChart = new Chart(ctxE, {
        type: "line",
        data: {
          labels: dummyLabels,
          datasets: [
            {
              data: initialEntropy,
              borderColor: "#00ffaa",
              borderWidth: 2,
              pointRadius: 0,
              fill: true,
              backgroundColor: "rgba(0, 255, 170, 0.08)"
            },
            {
              data: Array(MAX_POINTS).fill(7.8),
              borderColor: "rgba(255, 51, 102, 0.5)",
              borderWidth: 1,
              borderDash: [4, 4],
              pointRadius: 0
            }
          ]
        },
        options: { ...chartOpts, scales: { ...chartOpts.scales, y: { ...chartOpts.scales.y, min: 0, max: 8.5 } } }
      });
    }

    const ctxI = document.getElementById("ioCanvas")?.getContext("2d");
    if (ctxI) {
      ioChart = new Chart(ctxI, {
        type: "line",
        data: {
          labels: dummyLabels,
          datasets: [
            {
              data: initialIO,
              borderColor: "#00e5ff",
              borderWidth: 2,
              pointRadius: 0,
              fill: true,
              backgroundColor: "rgba(0, 229, 255, 0.08)"
            },
            {
              data: Array(MAX_POINTS).fill(50),
              borderColor: "rgba(255, 51, 102, 0.5)",
              borderWidth: 1,
              borderDash: [4, 4],
              pointRadius: 0
            }
          ]
        },
        options: { ...chartOpts, scales: { ...chartOpts.scales, y: { ...chartOpts.scales.y, min: 0, max: 300 } } }
      });
    }

    appendLog("AutoVault SOC Console active.", "info");
    startTelemetryLoop();
    connectWebSocketAgent();
  }

  // Terminal logging
  const logContainer = document.getElementById("terminalLog");
  function appendLog(msg, type = "info") {
    if (!logContainer) return;
    const timeStr = new Date().toTimeString().split(" ")[0];
    const div = document.createElement("div");
    div.className = `log-row log-row--${type}`;
    div.innerHTML = `<span style="color:#8e8e8e">[${timeStr}]</span> ${msg}`;
    logContainer.appendChild(div);
    logContainer.scrollTop = logContainer.scrollHeight;
  }

  document.getElementById("clearLogsBtn")?.addEventListener("click", () => {
    if (logContainer) logContainer.innerHTML = "";
  });

  // Telemetry loop
  let telemetryTimer = null;
  let isWsConnected = false;
  let ws = null;

  function updateTelemetry(entropy, ioVelocity) {
    if (entropyChart) {
      entropyChart.data.datasets[0].data.shift();
      entropyChart.data.datasets[0].data.push(entropy);
      entropyChart.update();
    }
    if (ioChart) {
      ioChart.data.datasets[0].data.shift();
      ioChart.data.datasets[0].data.push(ioVelocity);
      ioChart.update();
    }

    const entEl = document.getElementById("socEntropyVal");
    if (entEl) entEl.textContent = entropy.toFixed(2);
    const ioEl = document.getElementById("socIoVal");
    if (ioEl) ioEl.textContent = `${ioVelocity}/s`;
  }

  function startTelemetryLoop() {
    if (telemetryTimer) clearInterval(telemetryTimer);
    telemetryTimer = setInterval(() => {
      if (isWsConnected) return;
      const entropy = 3.0 + Math.random() * 0.9;
      const ioVel = Math.floor(6 + Math.random() * 8);
      updateTelemetry(entropy, ioVel);
    }, 1000);
  }

  function connectWebSocketAgent() {
    try {
      ws = new WebSocket("ws://localhost:8765");
      ws.onopen = () => {
        isWsConnected = true;
        document.getElementById("socDot").className = "dot dot--ok";
        document.getElementById("agentConnStatus").textContent = "CYBER DAEMON ONLINE";
        appendLog("Connected to Cyber Agent Daemon (ws://localhost:8765).", "info");
      };

      ws.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data);
          if (data.type === "telemetry") {
            updateTelemetry(data.entropy, data.io_velocity);
          } else if (data.type === "threat") {
            triggerThreatModal(data.entropy, data.io_velocity, data.process, data.pid);
          } else if (data.type === "lockdown") {
            appendLog(`[LOCKDOWN ENFORCED] Process suspended. IPFS CID: ${data.cid}`, "lockdown");
            document.getElementById("socCid").textContent = data.cid;
          }
        } catch (e) {}
      };

      ws.onclose = () => {
        isWsConnected = false;
        document.getElementById("socDot").className = "dot dot--warn";
        document.getElementById("agentConnStatus").textContent = "SIMULATION ONLINE";
        setTimeout(connectWebSocketAgent, 4000);
      };
    } catch (e) {}
  }

  /* -----------------------------------------------
     5. ADVANCED FEATURE 1: SHANNON ENTROPY CALCULATOR
  ----------------------------------------------- */
  function calculateShannonEntropy(str) {
    if (!str || str.length === 0) return 0;
    const len = str.length;
    const freq = {};
    for (let i = 0; i < len; i++) {
      const char = str[i];
      freq[char] = (freq[char] || 0) + 1;
    }

    let entropy = 0;
    for (const char in freq) {
      const p = freq[char] / len;
      entropy -= p * Math.log2(p);
    }
    return entropy;
  }

  const fileTextEditor = document.getElementById("fileTextEditor");
  const liveEntropyScore = document.getElementById("liveEntropyScore");
  const liveEntropyStatus = document.getElementById("liveEntropyStatus");
  const meterFillBar = document.getElementById("meterFillBar");
  const entropyResultPill = document.getElementById("entropyResultPill");

  function updateEntropyCalculator() {
    if (!fileTextEditor) return;
    const text = fileTextEditor.value;
    const entropy = calculateShannonEntropy(text);

    if (liveEntropyScore) liveEntropyScore.textContent = entropy.toFixed(2);
    if (entropyResultPill) entropyResultPill.textContent = `Entropy: ${entropy.toFixed(2)}`;

    const fillPct = Math.min(100, (entropy / 8.0) * 100);
    if (meterFillBar) meterFillBar.style.width = `${fillPct}%`;

    if (entropy >= 7.8) {
      if (liveEntropyStatus) {
        liveEntropyStatus.textContent = "Status: CRITICAL RANSOMWARE NOISE (HIGH ENTROPY)";
        liveEntropyStatus.style.color = "#ff3366";
      }
    } else if (entropy >= 5.5) {
      if (liveEntropyStatus) {
        liveEntropyStatus.textContent = "Status: HIGH DENSITY / COMPRESSED DATA";
        liveEntropyStatus.style.color = "#ffcc00";
      }
    } else {
      if (liveEntropyStatus) {
        liveEntropyStatus.textContent = "Status: NORMAL PLAIN TEXT / CODE";
        liveEntropyStatus.style.color = "#00ffaa";
      }
    }
  }

  fileTextEditor?.addEventListener("input", updateEntropyCalculator);

  // XOR Ransomware Simulator
  document.getElementById("runRansomwareXorBtn")?.addEventListener("click", () => {
    if (!fileTextEditor) return;
    const origText = fileTextEditor.value;
    let encryptedStr = "";
    for (let i = 0; i < origText.length; i++) {
      const randomByte = Math.floor(Math.random() * 256);
      encryptedStr += String.fromCharCode(randomByte);
    }
    fileTextEditor.value = encryptedStr;
    updateEntropyCalculator();
    appendLog("[ENTROPY LAB] File encrypted with simulated Ransomware XOR algorithm! Entropy jumped to ~7.95+", "threat");
  });

  document.getElementById("restoreSampleTextBtn")?.addEventListener("click", () => {
    if (!fileTextEditor) return;
    fileTextEditor.value = `CONFIDENTIAL CORPORATE DATA REPORT 2026\nStandard operating procedure and security policy documentation.\nAll remote file system connections must pass through multi-factor authentication.`;
    updateEntropyCalculator();
    appendLog("[ENTROPY LAB] Restored plain text sample file.", "info");
  });

  updateEntropyCalculator();

  /* -----------------------------------------------
     4. AUTOMATED RANSOMWARE FILE CREATOR & DROPZONE SECTOR
  ----------------------------------------------- */
  const generateRansomFileBtn = document.getElementById("generateRansomFileBtn");
  const autoSimulateAllBtn = document.getElementById("autoSimulateAllBtn");
  const fileDropzone = document.getElementById("fileDropzone");
  const fileInput = document.getElementById("fileInput");
  const scanResultBanner = document.getElementById("scanResultBanner");
  const scanResultText = document.getElementById("scanResultText");
  const dropzoneStatusBadge = document.getElementById("dropzoneStatusBadge");

  // A. Generate High-Entropy Ransomware Test File (.locked)
  generateRansomFileBtn?.addEventListener("click", () => {
    const buffer = new Uint8Array(2048);
    for (let i = 0; i < 2048; i++) {
      buffer[i] = Math.floor(Math.random() * 256);
    }
    const blob = new Blob([buffer], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ransomware_payload.locked";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (dropzoneStatusBadge) dropzoneStatusBadge.textContent = "Generated ransomware_payload.locked!";
    appendLog('[AUTOMATED SECTOR] Created high-entropy ransomware test file "ransomware_payload.locked" (Entropy: ~7.94)! Downloaded to browser.', "threat");
  });

  // B. Dropzone & File Input Handlers
  fileDropzone?.addEventListener("click", () => fileInput?.click());
  fileDropzone?.addEventListener("dragover", (e) => {
    e.preventDefault();
    fileDropzone.style.background = "rgba(2, 132, 199, 0.15)";
    fileDropzone.style.borderColor = "#00ffaa";
  });
  fileDropzone?.addEventListener("dragleave", () => {
    fileDropzone.style.background = "rgba(2, 132, 199, 0.06)";
    fileDropzone.style.borderColor = "#0284c7";
  });
  fileDropzone?.addEventListener("drop", (e) => {
    e.preventDefault();
    fileDropzone.style.background = "rgba(2, 132, 199, 0.06)";
    fileDropzone.style.borderColor = "#0284c7";
    if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
      processUploadedFile(e.dataTransfer.files[0]);
    }
  });

  fileInput?.addEventListener("change", (e) => {
    if (e.target?.files && e.target.files.length > 0) {
      processUploadedFile(e.target.files[0]);
    }
  });

  function processUploadedFile(file) {
    if (!file) return;
    if (scanResultBanner) {
      scanResultBanner.style.display = "flex";
      scanResultBanner.className = "phase-badge phase-badge--ok";
      if (scanResultText) scanResultText.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Scanning byte distribution of "${file.name}" (${file.size} bytes)...`;
    }

    const reader = new FileReader();
    reader.onload = function(evt) {
      const buffer = evt.target.result;
      const bytes = new Uint8Array(buffer);
      const len = bytes.length;
      let entropy = 0;

      if (len > 0) {
        const freq = new Array(256).fill(0);
        for (let i = 0; i < len; i++) {
          freq[bytes[i]]++;
        }
        for (let i = 0; i < 256; i++) {
          if (freq[i] > 0) {
            const p = freq[i] / len;
            entropy -= p * Math.log2(p);
          }
        }
      } else {
        entropy = 0;
      }

      const isThreat = (entropy >= 7.8) || (/\.(locked|enc|encrypted|crypto)$/i.test(file.name));

      setTimeout(() => {
        if (isThreat) {
          const actualEntropy = entropy > 0 ? entropy : 7.92;
          if (scanResultBanner) {
            scanResultBanner.className = "phase-badge phase-badge--danger";
            if (scanResultText) {
              scanResultText.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <strong>AUTOMATED TRIGGER: RANSOMWARE DETECTED IN "${file.name}"!</strong> Shannon Entropy: <strong>${actualEntropy.toFixed(2)} / 8.0</strong> &bull; Threat Threshold Exceeded &bull; Triggering AI Kill Switch & Alert Modal!`;
            }
          }
          if (dropzoneStatusBadge) {
            dropzoneStatusBadge.textContent = "THREAT DETECTED!";
            dropzoneStatusBadge.className = "badge badge--danger";
          }

          updateTelemetry(actualEntropy, 284);
          appendLog(`[AUTOMATED SECTOR] File "${file.name}" uploaded! High Shannon Entropy (${actualEntropy.toFixed(2)}) detected! Initiating process freeze & IPFS lockdown.`, "threat");
          triggerThreatModal(actualEntropy, 284, `malware_${file.name}`, Math.floor(1000 + Math.random() * 8000));
        } else {
          if (scanResultBanner) {
            scanResultBanner.className = "phase-badge phase-badge--ok";
            if (scanResultText) {
              scanResultText.innerHTML = `<i class="fa-solid fa-circle-check"></i> <strong>CLEAN FILE DETECTED in "${file.name}"</strong> &bull; Shannon Entropy: <strong>${entropy.toFixed(2)} / 8.0</strong> (Safe Range: 3.0 - 4.5). No ransomware noise found.`;
            }
          }
          if (dropzoneStatusBadge) {
            dropzoneStatusBadge.textContent = "CLEAN FILE DETECTED";
            dropzoneStatusBadge.className = "badge badge--ok";
          }
          appendLog(`[AUTOMATED SECTOR] File "${file.name}" analyzed. Shannon Entropy: ${entropy.toFixed(2)} (SAFE).`, "info");
        }
      }, 400);
    };

    reader.readAsArrayBuffer(file);
  }

  // C. 1-Click Auto-Simulate Attack (Create -> Upload -> Trigger Alert)
  autoSimulateAllBtn?.addEventListener("click", () => {
    appendLog("[AUTOMATED SECTOR] 1-Click Automated Ransomware Simulation Started...", "threat");
    if (dropzoneStatusBadge) dropzoneStatusBadge.textContent = "Automating Attack Flow...";
    
    const buffer = new Uint8Array(2048);
    for (let i = 0; i < 2048; i++) {
      buffer[i] = Math.floor(Math.random() * 256);
    }
    const fakeFile = new File([buffer], "automated_ransomware_payload.locked", { type: "application/octet-stream" });
    processUploadedFile(fakeFile);
  });

  /* -----------------------------------------------
     6. ADVANCED FEATURE 2: WEB3 CONTRACT SANDBOX
  ----------------------------------------------- */
  const txLogContent = document.getElementById("txLogContent");
  const contractStateText = document.getElementById("contractStateText");

  document.getElementById("triggerWeb3LockdownBtn")?.addEventListener("click", () => {
    const txHash = "0x" + Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join("");
    const cid = "QmAutoVaultEmergency_" + Math.random().toString(36).substring(2, 10);
    const blockNum = Math.floor(18000000 + Math.random() * 500000);

    if (txLogContent) {
      txLogContent.innerHTML = `
        <div style="color:#00ffaa;margin-bottom:4px">✓ TRANSACTION CONFIRMED (Block #${blockNum})</div>
        <div>Tx Hash: <span style="color:#00e5ff">${txHash}</span></div>
        <div>Event Emitted: <span style="color:#ff3366">LockdownTriggered("${cid}", ${Date.now()})</span></div>
        <div>Gas Used: 48,210 units (Polygon Amoy)</div>
      `;
    }
    if (contractStateText) {
      contractStateText.textContent = "COMPROMISED — EMERGENCY LOCKDOWN ACTIVE";
      contractStateText.style.color = "#ff3366";
    }

    document.getElementById("socCid").textContent = cid;
    document.getElementById("socTx").textContent = txHash.substring(0, 10) + "...";
    appendLog(`[WEB3] Contract AutoVaultRecovery.sol executed on Polygon Amoy. Tx: ${txHash.substring(0, 14)}...`, "lockdown");
  });

  document.getElementById("restoreWeb3StateBtn")?.addEventListener("click", () => {
    if (txLogContent) {
      txLogContent.innerHTML = `<div style="color:#00ffaa">✓ System state restored to CLEAN on Polygon Amoy.</div>`;
    }
    if (contractStateText) {
      contractStateText.textContent = "CLEAN (UNCOMPROMISED)";
      contractStateText.style.color = "#00ffaa";
    }
    appendLog("[WEB3] System restored to clean state.", "info");
  });

  /* -----------------------------------------------
     7. ATTACK SIMULATION CONTROLS
  ----------------------------------------------- */
  const threatPopup = document.getElementById("threatPopup");

  function triggerThreatModal(entropy = 7.94, io = 284, process = "malware_sim.exe", pid = 4920) {
    document.getElementById("popEntropy").textContent = entropy.toFixed(2);
    document.getElementById("popIo").textContent = `${io} ops/s`;
    document.getElementById("popProc").textContent = process;
    document.getElementById("popPid").textContent = pid;

    threatPopup.removeAttribute("hidden");
    appendLog(`[THREAT DETECTED] High entropy (${entropy.toFixed(2)}) by PID ${pid} (${process})!`, "threat");

    document.getElementById("bEnforcer").className = "phase-badge phase-badge--danger";
    document.getElementById("bEnforcer").innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> 3. Enforcer: <strong>SUSPENDING PID ${pid}</strong>`;
  }

  document.getElementById("attackSimBtn")?.addEventListener("click", () => {
    appendLog("Initiating simulated ransomware attack on test_vault...", "threat");
    if (isWsConnected && ws) {
      ws.send(JSON.stringify({ action: "simulate_attack" }));
    } else {
      triggerThreatModal(7.94, 284, "ransomware_sim.exe", 4920);
      updateTelemetry(7.94, 284);
    }
  });

  document.getElementById("popLockdownBtn")?.addEventListener("click", () => {
    threatPopup.setAttribute("hidden", "");
    const fakeCid = "QmAutoVaultLockdown_" + Math.random().toString(36).substring(2, 8);
    document.getElementById("socCid").textContent = fakeCid;
    appendLog(`[LOCKDOWN ENFORCED] Process suspended. Network isolated. Backup pinned to IPFS: ${fakeCid}`, "lockdown");

    document.getElementById("bEnforcer").className = "phase-badge phase-badge--ok";
    document.getElementById("bEnforcer").innerHTML = `<i class="fa-solid fa-check"></i> 3. Enforcer: <strong>KILL SWITCH ACTIVE</strong>`;

    document.getElementById("bVault").className = "phase-badge phase-badge--ok";
    document.getElementById("bVault").innerHTML = `<i class="fa-solid fa-vault"></i> 4. Vault: <strong>SNAPSHOT RESTORED FROM IPFS</strong>`;
  });

  document.getElementById("popDismissBtn")?.addEventListener("click", () => {
    threatPopup.setAttribute("hidden", "");
  });

  document.getElementById("resetSimBtn")?.addEventListener("click", () => {
    appendLog("Resetting security daemon & firewall rules...", "info");
    if (isWsConnected && ws) {
      ws.send(JSON.stringify({ action: "reset" }));
    }
    document.getElementById("bEnforcer").className = "phase-badge phase-badge--dim";
    document.getElementById("bEnforcer").innerHTML = `<i class="fa-solid fa-hand"></i> 3. Enforcer: <strong>STANDBY (0.2s KILL SWITCH)</strong>`;
    document.getElementById("bVault").className = "phase-badge phase-badge--dim";
    document.getElementById("bVault").innerHTML = `<i class="fa-solid fa-vault"></i> 4. Vault: <strong>READY FOR IMMUTABLE RECOVERY</strong>`;
    updateTelemetry(3.24, 12);
  });

  document.getElementById("manualSnapBtn")?.addEventListener("click", () => {
    const manualCid = "QmManualSnap_" + Math.random().toString(36).substring(2, 8);
    document.getElementById("socCid").textContent = manualCid;
    appendLog(`Manual snapshot pinned to IPFS: ${manualCid}`, "lockdown");
  });

  // Auto initialize SOC Charts on load
  initSOCCharts();

})();
