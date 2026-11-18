import tempfile
from pathlib import Path
import unittest
from app import add_expense, load_expenses, save_expenses, totals_by_category


class ExpenseTests(unittest.TestCase):
    def test_add_and_totals(self):
        items = []
        add_expense(items, "120.50", "Food", when="2026-11-18")
        add_expense(items, "20", "Food", when="2026-11-18")
        self.assertEqual(str(totals_by_category(items)["Food"]), "140.50")

    def test_invalid_amount(self):
        for amount in ("-1", "abc", "NaN", "0"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                add_expense([], amount, "Food")

    def test_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.json"
            items = []
            add_expense(items, 23, "Transport")
            save_expenses(path, items)
            self.assertEqual(load_expenses(path), items)

    def test_first_run(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(load_expenses(Path(folder) / "missing.json"), [])


if __name__ == "__main__":
    unittest.main()
