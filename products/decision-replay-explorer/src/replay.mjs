const MISSING = Symbol("missing");

export function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.keys(value).sort().reduce((out, key) => {
      out[key] = canonicalize(value[key]);
      return out;
    }, {});
  }
  return value;
}

export function stableStringify(value) {
  return JSON.stringify(canonicalize(value));
}

export async function sha256Hex(value) {
  const bytes = new TextEncoder().encode(stableStringify(value));
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, "0")).join("");
}

function printable(value) {
  if (value === MISSING) return "∅";
  if (typeof value === "string") return value;
  return JSON.stringify(value);
}

export function compareRecords(original, replay) {
  const differences = [];

  function walk(left, right, path) {
    if (left === MISSING || right === MISSING) {
      differences.push({
        state: left === MISSING ? "added" : "removed",
        path: path || "$",
        original: printable(left),
        replay: printable(right)
      });
      return;
    }

    const leftIsObject = left !== null && typeof left === "object";
    const rightIsObject = right !== null && typeof right === "object";

    if (!leftIsObject || !rightIsObject) {
      if (!Object.is(left, right)) {
        differences.push({
          state: "changed",
          path: path || "$",
          original: printable(left),
          replay: printable(right)
        });
      }
      return;
    }

    if (Array.isArray(left) || Array.isArray(right)) {
      if (!(Array.isArray(left) && Array.isArray(right))) {
        differences.push({
          state: "changed",
          path: path || "$",
          original: printable(left),
          replay: printable(right)
        });
        return;
      }
      const length = Math.max(left.length, right.length);
      for (let i = 0; i < length; i += 1) {
        walk(
          i < left.length ? left[i] : MISSING,
          i < right.length ? right[i] : MISSING,
          `${path}[${i}]`
        );
      }
      return;
    }

    const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
    for (const key of keys) {
      const childPath = path ? `${path}.${key}` : key;
      walk(
        Object.hasOwn(left, key) ? left[key] : MISSING,
        Object.hasOwn(right, key) ? right[key] : MISSING,
        childPath
      );
    }
  }

  walk(original, replay, "");
  return differences;
}

export function summarizeRecord(record) {
  const evidence = Array.isArray(record?.evidence_index)
    ? `${record.evidence_index.length} item${record.evidence_index.length === 1 ? "" : "s"}`
    : "not declared";

  const authority = record?.authority_cell?.id
    ?? record?.authority_cell_id
    ?? record?.authority?.id
    ?? "not declared";

  const evaluation = record?.verification?.status
    ?? record?.verification
    ?? record?.evaluation?.status
    ?? "not declared";

  const decision = record?.decision?.state
    ?? record?.decision_state
    ?? record?.state
    ?? "not declared";

  return { evidence, authority, evaluation, decision };
}

export function buildComparison(original, replay, originalHash, replayHash) {
  const differences = compareRecords(original, replay);
  return {
    schema: "kapukai.replay-comparison.v0.1",
    generated_at: new Date().toISOString(),
    equivalent: differences.length === 0,
    difference_count: differences.length,
    original_hash: originalHash,
    replay_hash: replayHash,
    differences
  };
}
