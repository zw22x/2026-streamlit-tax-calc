import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import dict_version as tax


class TaxCalculationTests(unittest.TestCase):
    def test_should_return_standard_deduction_when_filing_status_is_single(self):
        self.assertEqual(tax.calculate_deduction(tax.SINGLE), 16100)

    def test_should_return_standard_deduction_when_married_filing_jointly(self):
        self.assertEqual(tax.calculate_deduction((tax.MARRIED, "yes")), 32200)

    def test_should_floor_taxable_income_at_zero_when_income_below_deduction(self):
        self.assertEqual(tax.calculate_taxable_income(10_000, tax.SINGLE), 0)

    def test_should_calculate_taxable_income_when_income_exceeds_deduction(self):
        self.assertEqual(tax.calculate_taxable_income(50_000, tax.SINGLE), 33_900)

    def test_should_calculate_tax_when_taxable_income_matches_bracket(self):
        cases = [
            (12_400, tax.SINGLE, 1_240),
            (12_401, tax.SINGLE, 1_250.12),
            (97_800, (tax.MARRIED, "yes"), 11_240),
            (400_000, (tax.MARRIED, "no"), 109_082.25),
            (65_850, tax.HOH, 7_548),
            (700_000, tax.SINGLE, 214_957.25),
        ]

        for taxable_income, filing_status, expected_tax in cases:
            with self.subTest(taxable_income=taxable_income, filing_status=filing_status):
                self.assertAlmostEqual(
                    tax.calculate_tax(taxable_income, filing_status), expected_tax
                )

    def test_should_calculate_total_tax_when_married_filing_jointly(self):
        self.assertAlmostEqual(
            tax.calculate_total_tax(130_000, (tax.MARRIED, "yes")), 11_240
        )

    def test_should_calculate_total_tax_with_dependents_and_adoption_credit(self):
        self.assertAlmostEqual(
            tax.calculate_total_tax(
                100_000,
                tax.SINGLE,
                dependents=2,
                adoption_credit=True,
            ),
            8_314.60,
        )

    def test_should_raise_key_error_when_filing_status_is_invalid(self):
        with self.assertRaises(KeyError):
            tax.calculate_total_tax(50_000, "invalid")


def run_tests():
    print("\nTax Calculation Test Results")
    print("=" * 30)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TaxCalculationTests)
    result = unittest.TextTestRunner(
        stream=sys.stdout,
        verbosity=2,
        descriptions=True,
    ).run(suite)

    print("\nSummary")
    print("-" * 30)
    print(f"Tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    return result.wasSuccessful()


if __name__ == "__main__":
    if not run_tests():
        sys.exit(1)
