# Builds summaries and generates charts from stored transactions.
from categoriser import split_by_type
from parser import parse_csv

def net_saved(transactions):
    savings_moves = [t for t in transactions if "GBP Savings" in t["Description"]]
    return round(-sum(t["Amount"] for t in savings_moves), 2)

internal_keywords = ["savings", "investment", "pocket"]

def net_spent(transactions):
    card_payments = [t for t in transactions if t["Type"] == "Card Payment"]

    transfers_to_people = [
        t for t in transactions
        if t["Type"] == "Transfer"
        and t["Amount"] < 0
        and (t["Description"].startswith("To ") or "Transfer to" in t["Description"])
        and not any(word in t["Description"].lower() for word in internal_keywords)
    ]
    total = sum(t["Amount"] for t in card_payments + transfers_to_people)
    return round(-total, 2)

def net_topup(transactions):
    topup_moves = [t for t in transactions if "Topup"  in t["Type"]]
    return round(sum(t["Amount"] for t in topup_moves), 2)


if __name__ == "__main__":
    data = parse_csv("data/private/trackerBankStatement.csv")
    print("Net saved:", net_saved(data))
    print("Net spent:", net_spent(data))
    print("Net top-up:", net_topup(data))
