# EIS-LOWER-001B — Reference Evaluator and IR Conformance Tests

**Status:** Initial implementation for review. A passing reference evaluator is not, by itself, acceptance of 001A or physical qualification.

## Purpose

Provide an independent, backend-neutral executable interpretation of the v0.1.0 deterministic field and interference subset. This is the first software acceptance gate before any backend-specific lowerer is introduced.

## Contents

- `reference_evaluator.py`: standard-library arithmetic and graph-semantic evaluator; optionally validates the JSON Schema when the `jsonschema` package is installed.
- `test_reference_evaluator.py`: unit tests for the deterministic vectors, graph semantics, incompatible ports, and unresolved operands.

## Run

From the repository root:

```bash
python docs/EIS-LOWER-001B/reference_evaluator.py
python -m unittest discover -s docs/EIS-LOWER-001B -p 'test_*.py' -v
```

For a full Draft 2020-12 JSON Schema check, install `jsonschema` in the test environment:

```bash
python -m pip install 'jsonschema>=4.18'
python docs/EIS-LOWER-001B/reference_evaluator.py
```

The evaluator emits a JSON report with source digests, individual vector results, semantic graph checks, schema-check status, and limitations. Exit status is zero only when all performed checks pass.

## Scope and limitations

The evaluator implements only:
- complex field values represented by real and imaginary components;
- two-input coherent field addition;
- ideal squared-magnitude intensity;
- the declared cross-term identity;
- graph reference, port direction, and port-domain checks.

It does not model a physical interferometer transfer matrix, coupler imbalance, propagation loss, phase drift, detector responsivity, balanced subtraction, noise, thermal/electrical effects, KKA modulator behavior, foundry process variation, or layout. It does not establish a physical or backend conformance claim.

The v0.1.0 schema currently describes a broader set of node and operation kinds than this reference evaluator executes. Unsupported operation kinds fail explicitly rather than being silently approximated. Semantic graph checks supplement JSON Schema; JSON Schema alone does not enforce unique IDs, valid references, or port compatibility.

## 001B acceptance criteria

1. All six deterministic interference vectors pass at the declared tolerances.
2. The example network passes structural schema validation when `jsonschema` is available.
3. The example network passes semantic graph validation.
4. Negative tests demonstrate rejection of incompatible port domains and unresolved operands.
5. The emitted report identifies the exact IR and vector-suite digests and states the evaluator's limitations.

A passing report is evidence for this reference implementation only. A second independent reader and a backend-specific conformance path remain subsequent work.
