const RING_CIRCUMFERENCE = 2 * Math.PI * 52;

const form = document.getElementById("scan-form");
const urlInput = document.getElementById("url-input");
const scanBtn = document.getElementById("scan-btn");
const btnText = scanBtn.querySelector(".btn-text");
const btnSpinner = scanBtn.querySelector(".btn-spinner");
const formError = document.getElementById("form-error");
const results = document.getElementById("results");
const threatScore = document.getElementById("threat-score");
const ringFill = document.getElementById("ring-fill");
const riskBadge = document.getElementById("risk-badge");
const scannedUrl = document.getElementById("scanned-url");
const scanTime = document.getElementById("scan-time");
const findingsList = document.getElementById("findings-list");
const historyList = document.getElementById("history-list");

function setLoading(loading) {
  scanBtn.disabled = loading;
  btnText.hidden = loading;
  btnSpinner.hidden = !loading;
}

function showError(message) {
  formError.textContent = message;
  formError.hidden = !message;
}

function updateRing(score, color) {
  const offset = RING_CIRCUMFERENCE - (score / 100) * RING_CIRCUMFERENCE;
  ringFill.style.strokeDashoffset = offset;
  ringFill.style.stroke = color;
}

function formatTime(iso) {
  return new Date(iso).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function renderFindings(findings, threatScoreValue) {
  findingsList.innerHTML = "";

  if (!findings.length && threatScoreValue === 0) {
    const li = document.createElement("li");
    li.className = "finding-item finding-safe";
    li.textContent = "No suspicious indicators detected.";
    findingsList.appendChild(li);
    return;
  }

  findings.forEach((f) => {
    const li = document.createElement("li");
    li.className = "finding-item";
    li.innerHTML = `
      <span class="finding-score">+${f.score}</span>
      <span>${escapeHtml(f.description)}</span>
    `;
    findingsList.appendChild(li);
  });
}

function renderResult(data) {
  results.hidden = false;
  threatScore.textContent = data.threat_score;
  updateRing(data.threat_score, data.risk_color);
  riskBadge.textContent = data.risk_label;
  riskBadge.style.background = `${data.risk_color}22`;
  riskBadge.style.color = data.risk_color;
  scannedUrl.textContent = data.url;
  scanTime.textContent = `Scanned ${formatTime(new Date().toISOString())}`;
  renderFindings(data.findings, data.threat_score);
}

function renderHistory(scans) {
  historyList.innerHTML = "";

  if (!scans.length) {
    const li = document.createElement("li");
    li.className = "history-empty";
    li.textContent = "No scans yet. Analyze a URL to get started.";
    historyList.appendChild(li);
    return;
  }

  scans.forEach((scan) => {
    const li = document.createElement("li");
    li.className = "history-item";
    li.innerHTML = `
      <p class="history-url">${escapeHtml(scan.url)}</p>
      <div class="history-meta">
        <span class="history-score" style="color:${scan.risk_color}">${scan.threat_score} — ${escapeHtml(scan.risk_label)}</span>
        <span>${formatTime(scan.scanned_at)}</span>
      </div>
    `;
    li.addEventListener("click", () => {
      urlInput.value = scan.url;
      renderResult(scan);
    });
    historyList.appendChild(li);
  });
}

function escapeHtml(text) {
  const el = document.createElement("div");
  el.textContent = text;
  return el.innerHTML;
}

async function loadHistory() {
  try {
    const res = await fetch("/api/history");
    const data = await res.json();
    renderHistory(data.scans || []);
  } catch {
    /* history is optional */
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");

  const url = urlInput.value.trim();
  if (!url) {
    showError("Please enter a URL to scan.");
    return;
  }

  setLoading(true);

  try {
    const res = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await res.json();

    if (!data.is_valid) {
      showError(data.error || "Invalid URL.");
      results.hidden = true;
      return;
    }

    renderResult(data);
    await loadHistory();
  } catch {
    showError("Scan failed. Please try again.");
  } finally {
    setLoading(false);
  }
});

loadHistory();
