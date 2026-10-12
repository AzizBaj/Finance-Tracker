#seperate transfers, withdrawals, deposits, and fees into different categories
from parser import parse_csv
from collections import defaultdict   

def split_by_type(transactions):
    groups = defaultdict(list)
    for transaction in transactions:
        groups[transaction["Type"]].append(transaction)
    return groups

if __name__ == "__main__":
    data = parse_csv("data/private/trackerBankStatement.csv")
    groups = split_by_type(data)

    for type_name, items in groups.items():
        print(type_name, len(items))

    print(sum(len(items) for items in groups.values()))