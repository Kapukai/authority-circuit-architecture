import { sha256Hex, compareRecords, summarizeRecord, buildComparison } from "./replay.mjs";

const $ = selector => document.querySelector(selector);
const originalFile = $("#originalFile");
const replayFile = $("#replayFile");
const demoButton = $("#demoButton");
const exportButton = $("#exportButton");
const errorMessage = $("#errorMessage");
const statusBadge = $("#statusBadge");
const diffBody = $("#diffBody");
const emptyState = $("#emptyState");
const tableWrap = $("#tableWrap");

let originalRecord = null;
let replayRecord = null;
let currentComparison = null;
let activeFilter = "all";

async function readJson(file) {
  try {
    return JSON.parse(await file.text());
  } catch (error) {
    throw new Error(`${file.name}: invalid JSON (${error.message})`);
  }
}

function displayError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function clearError() {
  errorMessage.hidden = true;
  errorMessage.textContent = "";
}

function setBadge(label, state) {
  statusBadge.textContent = label;
  statusBadge.className = `badge ${state}`;
}

function formatValue(value) {
  const text = String(value);
  return text.length > 180 ? `${text.slice(0, 177)}…` : text;
}

function renderDifferences(differences) {
  const visible = activeFilter === "all"
    ? differences
    : differences.filter(item => item.state === activeFilter);

  diffBody.replaceChildren();

  for (const item of visible) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><span class="state ${item.state}">${item.state.toUpperCase()}</span></td>
      <td><code>${escapeHtml(item.path)}</code></td>
      <td><pre>${escapeHtml(formatValue(item.original))}</pre></td>
      <td><pre>${escapeHtml(formatValue(item.replay))}</pre></td>`;
    diffBody.append(row);
  }

  if (differences.length === 0) {
    emptyState.textContent = "No differences observed. The supplied records are structurally equivalent.";
    emptyState.hidden = false;
    tableWrap.hidden = true;
  } else if (visible.length === 0) {
    emptyState.textContent = `No ${activeFilter} paths observed.`;
    emptyState.hidden = false;
    tableWrap.hidden = true;
  } else {
    emptyState.hidden = true;
    tableWrap.hidden = false;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function evaluate() {
  if (!originalRecord || !replayRecord) return;

  clearError();

  const [originalHash, replayHash] = await Promise.all([
    sha256Hex(originalRecord),
    sha256Hex(replayRecord)
  ]);
  const differences = compareRecords(originalRecord, replayRecord);
  currentComparison = buildComparison(originalRecord, replayRecord, originalHash, replayHash);

  $("#originalHash").textContent = originalHash;
  $("#replayHash").textContent = replayHash;
  $("#differenceCount").textContent = String(differences.length);
  $("#equivalence").textContent = differences.length === 0 ? "EQUIVALENT" : "DIVERGENT";

  const summary = summarizeRecord(originalRecord);
  $("#evidenceState").textContent = summary.evidence;
  $("#authorityState").textContent = summary.authority;
  $("#evaluationState").textContent = summary.evaluation;
  $("#decisionState").textContent = summary.decision;
  $("#replayState").textContent = differences.length === 0 ? "PASS" : "REVIEW";

  setBadge(
    differences.length === 0 ? "REPLAY EQUIVALENT" : "REPLAY DIVERGENT",
    differences.length === 0 ? "pass" : "fail"
  );
  exportButton.disabled = false;
  renderDifferences(differences);
}

originalFile.addEventListener("change", async event => {
  try {
    originalRecord = await readJson(event.target.files[0]);
    await evaluate();
  } catch (error) {
    displayError(error.message);
  }
});

replayFile.addEventListener("change", async event => {
  try {
    replayRecord = await readJson(event.target.files[0]);
    await evaluate();
  } catch (error) {
    displayError(error.message);
  }
});

demoButton.addEventListener("click", async () => {
  try {
    const [originalResponse, replayResponse] = await Promise.all([
      fetch("./examples/original.dpr.json"),
      fetch("./examples/replay.dpr.json")
    ]);
    originalRecord = await originalResponse.json();
    replayRecord = await replayResponse.json();
    await evaluate();
  } catch {
    displayError("The demonstration requires a local web server. Run: python3 -m http.server 8080");
  }
});

exportButton.addEventListener("click", () => {
  if (!currentComparison) return;
  const blob = new Blob([JSON.stringify(currentComparison, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "replay-comparison.json";
  anchor.click();
  URL.revokeObjectURL(url);
});

document.querySelectorAll(".filter").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    activeFilter = button.dataset.filter;
    if (currentComparison) renderDifferences(currentComparison.differences);
  });
});
