# Reads bank CSV exports and normalises them into a consistent transaction format.
#first remove any declined payments
#10 different collums
import csv
from datetime import datetime 

def parse_csv(path):
    transactions = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["State"] == "COMPLETED":
                transactions.append({
                                "Type": row["Type"].strip(),#string
                                "Product": row["Product"].strip(),#string
                                "Started Date": datetime.strptime(row["Started Date"], "%Y-%m-%d %H:%M:%S").date(),#date
                                "Description": row["Description"].strip(),#string
                                "Amount": float(row["Amount"]),#float
                                "Currency": row["Currency"].strip(),#string
                            })
             

            
    return transactions
if __name__ == "__main__":
    data = parse_csv("data/private/trackerBankStatement.csv")
    print(len(data))
    print(data[0]["Amount"])
