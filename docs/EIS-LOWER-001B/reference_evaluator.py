#!/usr/bin/env python3
"""Backend-independent reference evaluator for EIS-LOWER-001A v0.1.0.

Uses only the Python standard library for semantic checks and arithmetic.
If jsonschema is installed, also validates the JSON Schema.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def close(actual: float, expected: float, absolute: float, relative: float) -> bool:
    return math.isclose(actual, expected, abs_tol=absolute, rel_tol=relative)


def evaluate_vectors(suite: dict[str, Any]) -> list[dict[str, Any]]:
    tol = suite["quantity_convention"]["tolerance"]
    absolute, relative = tol["absolute"], tol["relative"]
    results = []
    for vector in suite["vectors"]:
        a = complex(vector["A"]["re"], vector["A"]["im"])
        b = complex(vector["B"]["re"], vector["B"]["im"])
        intensity = abs(a + b) ** 2
        cross = 2.0 * (a * b.conjugate()).real
        expected_i = vector["expected"]["intensity"]
        expected_c = vector["expected"]["cross_term"]
        results.append({
            "id": vector["id"],
            "actual": {"intensity": intensity, "cross_term": cross},
            "expected": {"intensity": expected_i, "cross_term": expected_c},
            "absolute_error": {
                "intensity": abs(intensity - expected_i),
                "cross_term": abs(cross - expected_c),
            },
            "pass": close(intensity, expected_i, absolute, relative)
                    and close(cross, expected_c, absolute, relative),
        })
    return results


def validate_graph(ir: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    nodes = ir.get("nodes", [])
    node_map: dict[str, dict[str, Any]] = {}
    for node in nodes:
        node_id = node.get("node_id")
        if not node_id:
            errors.append("node missing node_id")
            continue
        if node_id in node_map:
            errors.append(f"duplicate node_id: {node_id}")
        node_map[node_id] = node

    def port(node_id: str, port_id: str) -> dict[str, Any] | None:
        node = node_map.get(node_id)
        if node is None:
            return None
        matches = [p for p in node.get("ports", []) if p.get("port_id") == port_id]
        if len(matches) != 1:
            errors.append(f"{node_id}.{port_id}: expected exactly one declared port")
            return None
        return matches[0]

    for connection in ir.get("connections", []):
        source_id, target_id = connection.get("from_node"), connection.get("to_node")
        source = port(source_id, connection.get("from_port"))
        target = port(target_id, connection.get("to_port"))
        if source is None or target is None:
            continue
        if source.get("direction") != "output":
            errors.append(f"{source_id}.{connection.get('from_port')}: connection source is not output")
        if target.get("direction") != "input":
            errors.append(f"{target_id}.{connection.get('to_port')}: connection target is not input")
        if source.get("domain") != target.get("domain"):
            errors.append(f"{source_id} -> {target_id}: incompatible port domains")

    # All coherent fields in v0.1.0 share the network's declared phase reference.
    reference = ir.get("conventions", {}).get("phase_reference_id")
    if not reference:
        errors.append("missing network phase_reference_id")

    values: dict[str, complex | float] = {}
    for node in nodes:
        if node.get("kind") == "field_source" and "field_value" in node:
            fv = node["field_value"]
            values[f'{node["node_id"]}.field_value'] = complex(fv["re"], fv["im"])

    for operation in ir.get("operations", []):
        kind = operation.get("kind")
        operands = operation.get("operands", [])
        result = operation.get("result")
        if kind == "complex_field_sum":
            if len(operands) != 2:
                errors.append(f'{operation.get("operation_id")}: complex_field_sum requires 2 operands')
                continue
            if not all(op in values and isinstance(values[op], complex) for op in operands):
                errors.append(f'{operation.get("operation_id")}: unresolved or non-complex field operand')
                continue
            values[result] = values[operands[0]] + values[operands[1]]
        elif kind == "field_intensity":
            if len(operands) != 1:
                errors.append(f'{operation.get("operation_id")}: field_intensity requires 1 operand')
                continue
            value = values.get(operands[0])
            if not isinstance(value, complex):
                errors.append(f'{operation.get("operation_id")}: unresolved or non-complex field operand')
                continue
            values[result] = abs(value) ** 2
        elif kind == "complex_interference_intensity":
            if len(operands) != 2:
                errors.append(f'{operation.get("operation_id")}: complex_interference_intensity requires 2 operands')
                continue
            if not all(op in values and isinstance(values[op], complex) for op in operands):
                errors.append(f'{operation.get("operation_id")}: unresolved or non-complex field operand')
                continue
            a, b = values[operands[0]], values[operands[1]]
            values[result] = abs(a + b) ** 2
        else:
            errors.append(f'{operation.get("operation_id")}: operation not executable by v0.1.0 reference evaluator: {kind}')

    for operation in ir.get("operations", []):
        result = operation.get("result")
        if result not in values:
            errors.append(f'{operation.get("operation_id")}: result was not evaluated ({result})')
    return errors


def schema_check(schema: dict[str, Any], ir: dict[str, Any]) -> dict[str, Any]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return {"available": False, "pass": None, "errors": [],
                "note": "Install jsonschema to run the Draft 2020-12 structural schema check."}
    validator = jsonschema.Draft202012Validator(schema)
    errors = [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
              for e in validator.iter_errors(ir)]
    return {"available": True, "pass": not errors, "errors": errors}


def build_report(root: Path) -> dict[str, Any]:
    base = root / "docs" / "EIS-LOWER-001A"
    schema = load_json(base / "schema" / "photonic-network-ir.schema.json")
    ir = load_json(base / "examples" / "two-field-interference.json")
    suite = load_json(base / "test-vectors" / "interference-v1.json")
    vector_results = evaluate_vectors(suite)
    graph_errors = validate_graph(ir)
    structural = schema_check(schema, ir)
    return {
        "report_id": "EIS-LOWER-001B-CONFORMANCE",
        "report_version": "0.1.0",
        "evaluator": {"name": "EIS-LOWER-001B-reference-evaluator",
                      "version": "0.1.0", "python": platform.python_version()},
        "source": {"schema_version": ir["schema_version"],
                   "network_id": ir["network_id"],
                   "ir_sha256": canonical_digest(ir),
                   "vector_suite_id": suite["suite_id"],
                   "vector_suite_sha256": canonical_digest(suite)},
        "checks": {
            "json_schema": structural,
            "semantic_graph": {"pass": not graph_errors, "errors": graph_errors},
            "reference_vectors": {"pass": all(v["pass"] for v in vector_results),
                                  "passed": sum(v["pass"] for v in vector_results),
                                  "total": len(vector_results),
                                  "results": vector_results},
        },
        "overall_status": "PASS" if (
            not graph_errors
            and all(v["pass"] for v in vector_results)
            and structural["pass"] is not False
        ) else "FAIL",
        "limitations": [
            "A missing jsonschema package leaves structural schema validation unperformed.",
            "This evaluator covers only the v0.1.0 deterministic ideal-field subset.",
            "It does not establish physical accuracy, detector behavior, foundry compatibility, or backend conformance.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3],
                        help="repository root (defaults to inferred repository root)")
    parser.add_argument("--output", type=Path, help="optional path for JSON conformance report")
    args = parser.parse_args()
    report = build_report(args.root)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
