const predicates = [
  { id: "A", name: "Authority valid", value: "TRUE" },
  { id: "J", name: "Jurisdiction", value: "TRUE" },
  { id: "R", name: "Rule applicable", value: "TRUE" },
  { id: "E", name: "Evidence sufficient", value: "UNKNOWN" },
  { id: "P", name: "Procedure complete", value: "TRUE" },
  { id: "T", name: "Time valid", value: "TRUE" },
  { id: "N", name: "Notice and review", value: "TRUE" },
  { id: "C", name: "Conflict present", value: "FALSE" },
  { id: "V", name: "Revoked/prohibited", value: "FALSE" }
];

const values = ["TRUE", "FALSE", "UNKNOWN", "CONFLICTED", "EXPIRED", "REVOKED"];
const grid = document.querySelector("#predicate-grid");
const stateOutput = document.querySelector("#decision-state");
const noteOutput = document.querySelector("#decision-note");
const downloadButton = document.querySelector("#download-dpr");

function renderPredicates() {
  grid.innerHTML = "";
  predicates.forEach((predicate) => {
    const wrapper = document.createElement("div");
    wrapper.className = "predicate";

    const label = document.createElement("label");
    label.htmlFor = `predicate-${predicate.id}`;
    label.innerHTML = `<span>${predicate.name}</span><code>${predicate.id}</code>`;

    const select = document.createElement("select");
    select.id = `predicate-${predicate.id}`;
    select.setAttribute("aria-label", `${predicate.name} value`);

    values.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      option.selected = value === predicate.value;
      select.append(option);
    });

    select.addEventListener("change", (event) => {
      predicate.value = event.target.value;
      evaluate();
    });

    wrapper.append(label, select);
    grid.append(wrapper);
  });
}

function evaluate() {
  const byId = Object.fromEntries(predicates.map((item) => [item.id, item.value]));
  let state = "DENY";
  let note = "At least one required predicate is false, expired, or otherwise unsatisfied.";

  if (byId.V === "TRUE" || byId.V === "REVOKED") {
    state = "REVOKED";
    note = "A declared revocation or prohibition takes precedence over ordinary authorization.";
  } else if (byId.C === "TRUE" || predicates.some((item) => item.value === "CONFLICTED")) {
    state = "CONFLICT";
    note = "A material input is conflicted. The contradiction must remain visible and be resolved.";
  } else if (predicates.some((item) => item.value === "UNKNOWN")) {
    state = "HOLD";
    note = "A mandatory predicate is unknown. ALLOW is blocked pending verification.";
  } else if (predicates.some((item) => item.value === "REVOKED")) {
    state = "REVOKED";
    note = "A material input is revoked. The decision cannot proceed as ordinary authorization.";
  } else if (predicates.some((item) => item.value === "EXPIRED")) {
    state = "DENY";
    note = "A material input is expired and does not satisfy the declared synthetic profile.";
  } else {
    const requiredTrue = ["A", "J", "R", "E", "P", "T", "N"].every((id) => byId[id] === "TRUE");
    const blockersClear = byId.C === "FALSE" && byId.V === "FALSE";
    if (requiredTrue && blockersClear) {
      state = "ALLOW";
      note = "All mandatory synthetic predicates are true and declared blockers are clear.";
    }
  }

  stateOutput.value = state;
  stateOutput.textContent = state;
  stateOutput.className = `decision ${state.toLowerCase()}`;
  noteOutput.textContent = note;
  return { state, note };
}

function downloadProofRecord() {
  const evaluation = evaluate();
  const record = {
    notice: "Illustrative synthetic output. Not an ACA conformance claim or real-world authority determination.",
    record_id: `DPR-synthetic-${new Date().toISOString().replaceAll(/[-:.TZ]/g, "").slice(0, 14)}`,
    profile_id: "ACA-WD01-SYNTHETIC-ELIGIBILITY",
    rule_version: "0.1.0-working-draft",
    evaluated_at: new Date().toISOString(),
    state: evaluation.state,
    predicates: predicates.map((item) => ({
      id: item.id,
      value: item.value,
      source: "synthetic-user-selected-input"
    })),
    transition_reason: evaluation.note,
    remedy: {
      status: evaluation.state === "ALLOW" ? "NONE" : "AVAILABLE",
      route: evaluation.state === "ALLOW" ? "not-applicable" : "verify-or-correct-material-input",
      deadline: null
    }
  };

  const blob = new Blob([`${JSON.stringify(record, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ACA-illustrative-decision-proof-record.json";
  link.click();
  URL.revokeObjectURL(url);
}

renderPredicates();
evaluate();
downloadButton.addEventListener("click", downloadProofRecord);
