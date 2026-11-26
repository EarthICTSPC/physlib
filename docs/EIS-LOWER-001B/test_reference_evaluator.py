"""Unit tests for EIS-LOWER-001B reference evaluator."""
import json
import unittest
from pathlib import Path

from reference_evaluator import evaluate_vectors, validate_graph


BASE = Path(__file__).resolve().parents[1] / "EIS-LOWER-001A"


class ReferenceEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.suite = json.loads((BASE / "test-vectors" / "interference-v1.json").read_text())
        cls.ir = json.loads((BASE / "examples" / "two-field-interference.json").read_text())

    def test_all_reference_vectors_pass(self):
        results = evaluate_vectors(self.suite)
        self.assertEqual(len(results), 6)
        self.assertTrue(all(result["pass"] for result in results), results)

    def test_general_complex_pair_exact_expected_value(self):
        vector = next(v for v in self.suite["vectors"] if v["id"] == "general_complex_pair")
        self.assertEqual(vector["expected"]["intensity"], 0.125)
        result = next(r for r in evaluate_vectors(self.suite) if r["id"] == "general_complex_pair")
        self.assertTrue(result["pass"], result)

    def test_example_graph_is_semantically_valid(self):
        self.assertEqual(validate_graph(self.ir), [])

    def test_incompatible_connection_domain_is_rejected(self):
        broken = json.loads(json.dumps(self.ir))
        broken["connections"][0]["to_port"] = "intensity"
        errors = validate_graph(broken)
        self.assertTrue(any("incompatible port domains" in error for error in errors), errors)

    def test_unresolved_operation_operand_is_rejected(self):
        broken = json.loads(json.dumps(self.ir))
        broken["operations"][0]["operands"][0] = "missing.field"
        errors = validate_graph(broken)
        self.assertTrue(any("unresolved or non-complex" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
