import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from datetime import date


def load_expenses(path):
    path = Path(path)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expense data must be a list")
    return data


def add_expense(items, amount, category, note="", when=None):
    try:
        value = Decimal(str(amount))
    except InvalidOperation as exc:
        raise ValueError("Amount must be numeric") from exc
    if not value.is_finite() or value <= 0:
        raise ValueError("Amount must be positive and finite")
    if not category.strip():
        raise ValueError("Category cannot be blank")
    record = {"id": max((i["id"] for i in items), default=0) + 1,
              "date": when or date.today().isoformat(), "amount": str(value),
              "category": category.strip(), "note": note.strip()}
    items.append(record)
    return record


def totals_by_category(items):
    totals = {}
    for item in items:
        category = item["category"]
        totals[category] = totals.get(category, Decimal("0")) + Decimal(item["amount"])
    return totals


def save_expenses(path, items):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(items, indent=2), encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description="Expense tracker (amounts in NGN)")
    parser.add_argument("--file", default="expenses.json")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")
    sub.add_parser("list")
    sub.add_parser("summary")
    args = parser.parse_args()
    try:
        items = load_expenses(args.file)
        if args.command == "add":
            record = add_expense(items, args.amount, args.category, args.note)
            save_expenses(args.file, items)
            print(f"Saved expense #{record['id']}")
        elif args.command == "list":
            for i in items:
                print(f"#{i['id']} {i['date']} NGN {i['amount']} {i['category']} — {i['note']}")
            if not items:
                print("No expenses yet")
        else:
            totals = totals_by_category(items)
            for category, total in sorted(totals.items()):
                print(f"{category}: NGN {total:.2f}")
            print(f"TOTAL: NGN {sum(totals.values(), Decimal('0')):.2f}")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
