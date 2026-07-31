import assert from "node:assert/strict";
import { compareRecords, canonicalize, stableStringify, summarizeRecord } from "../src/replay.mjs";

assert.deepEqual(canonicalize({z: 1, a: {b: 2, a: 1}}), {a: {a: 1, b: 2}, z: 1});
assert.equal(stableStringify({b: 2, a: 1}), '{"a":1,"b":2}');
assert.deepEqual(compareRecords({a: 1}, {a: 1}), []);

const changes = compareRecords(
  {a: 1, b: [1, 2], removed: true},
  {a: 2, b: [1, 3], added: true}
);
assert.deepEqual(changes.map(x => [x.state, x.path]), [
  ["changed", "a"],
  ["added", "added"],
  ["changed", "b[1]"],
  ["removed", "removed"]
]);

assert.deepEqual(
  summarizeRecord({
    evidence_index: [{id: 1}],
    authority_cell: {id: "ACA-1"},
    verification: {status: "PASS"},
    decision: {state: "ELIGIBLE"}
  }),
  {evidence: "1 item", authority: "ACA-1", evaluation: "PASS", decision: "ELIGIBLE"}
);

console.log("PASS replay.test.mjs");
