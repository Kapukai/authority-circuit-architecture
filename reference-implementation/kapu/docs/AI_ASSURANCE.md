# AI Assurance Boundary

## Deterministic core

Final ACA state resolution, DPR hashing, chain verification, and replay comparison
are deterministic code paths. They do not call an AI model.

## AI-assisted inputs

An AI system may propose extracted predicates, classifications, explanations, or
evidence links. Those outputs remain quarantined until:

1. the output is schema-valid;
2. model, prompt, and output hashes are recorded;
3. authority and evidence references are independently checked;
4. applicable negative and adversarial tests pass;
5. required human review is completed.

AI output is never treated as legal, organizational, or operational authority
merely because a model produced it.
