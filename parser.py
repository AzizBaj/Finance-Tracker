# Reads bank CSV exports and normalises them into a consistent transaction format.
#first remove any declined payments
#10 different collums
import csv

def parse_csv(path):
    transactions = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["State"] == "COMPLETED":
                transactions.append({
                                "Type": row["Type"],
                                "Product": row["Product"],
                                "Started Date": row["Started Date"],
                                "Description": row["Description"],
                                "Amount": row["Amount"],
                                "Currency": row["Currency"],
                            })
             

            
    return transactions
if __name__ == "__main__":
    data = parse_csv("data/private/trackerBankStatement.csv")
    print(len(data))
    print(data[0])
