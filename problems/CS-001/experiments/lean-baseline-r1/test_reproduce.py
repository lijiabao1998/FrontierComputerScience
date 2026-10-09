import unittest
from reproduce import parse_axioms, source_inventory, ALLOWED, classify_replay

class HarnessTests(unittest.TestCase):
    def test_no_axioms(self):
        self.assertEqual(parse_axioms("'Term.constFold_equiv' does not depend on any axioms\n"), set())
    def test_allowed_axioms(self):
        self.assertTrue(parse_axioms("'Term.constFold_equiv' depends on axioms: [propext, Quot.sound]") <= ALLOWED)
    def test_sorry_is_rejected(self):
        self.assertFalse(parse_axioms("'Term.constFold_equiv' depends on axioms: [sorryAx]") <= ALLOWED)
    def test_custom_axiom_is_rejected(self):
        self.assertFalse(parse_axioms("'Term.constFold_equiv' depends on axioms: [myAxiom]") <= ALLOWED)
    def test_native_axiom_is_rejected(self):
        self.assertFalse(parse_axioms("'Term.constFold_equiv' depends on axioms: [Lean.ofReduceBool]") <= ALLOWED)
    def test_missing_exact_target_fails(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Other' does not depend on any axioms")
    def test_duplicate_target_fails(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Term.constFold_equiv' does not depend on any axioms\n" * 2)
    def test_classification_all_pass(self):
        self.assertEqual(classify_replay(True, 'PASS'), ('PASS', 0))
    def test_classification_closure_fail_is_partial(self):
        self.assertEqual(classify_replay(True, 'FAIL'), ('PARTIAL', 3))
    def test_classification_closure_not_run_is_partial(self):
        self.assertEqual(classify_replay(True, 'NOT_RUN'), ('PARTIAL', 3))
    def test_classification_core_fail(self):
        self.assertEqual(classify_replay(False, 'PASS'), ('FAIL', 1))
    def test_pinned_inventory(self):
        inventory = source_inventory()
        self.assertEqual(inventory['external_lake_packages'], [])
        self.assertEqual(inventory['explicit_imports'], [])
        self.assertEqual(inventory['source_modules'], ['VerifiedCompiler'])

if __name__ == '__main__':
    unittest.main()
