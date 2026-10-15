# Builds summaries and generates charts from stored transactions.
from categoriser import split_by_type
from parser import parse_csv
from collections import defaultdict   
from datetime import date

internal_keywords = ["savings", "investment", "pocket"]
def get_spending(transactions):
    spending = []
    for t in transactions:
        description = t["Description"]
        if t["Type"] == "Card Payment":
            spending.append(t)
        elif (
            t["Type"] == "Transfer"
            and t["Amount"] < 0
            and (description.startswith("To ") or "Transfer to" in description)
            and not any(word in description.lower() for word in internal_keywords)
        ):
            spending.append(t)
    return spending

#calculates total saved by searching the decription of each transaction
def net_saved(transactions):
    savings_moves = [t for t in transactions if "GBP Savings" in t["Description"]]
    return round(-sum(t["Amount"] for t in savings_moves), 2)

#calculates total spent by searching for card payments and transfers to other accounts while removing internal transfers between own accounts
internal_keywords = ["savings", "investment", "pocket"]
def net_spent(transactions):
    #adds all card payments to a list
    card_payments = [t for t in transactions if t["Type"] == "Card Payment"]
#uses keywords to filter out any internal transfers between own accounts and adds the rest to a list
    transfers_to_people = [
        t for t in transactions
        if t["Type"] == "Transfer"
        and t["Amount"] < 0
        and (t["Description"].startswith("To ") or "Transfer to" in t["Description"])
        and not any(word in t["Description"].lower() for word in internal_keywords)
    ]
    #adds the two together
    total = sum(t["Amount"] for t in card_payments + transfers_to_people)
    return round(-total, 2)

#net amount of money moved into account from payments and transfers
def net_topup(transactions):
    topup_moves = [t for t in transactions if "Topup"  in t["Type"]]
    return round(sum(t["Amount"] for t in topup_moves), 2)

def Descript_amount_dict(transactions):
     #creates dict with float values and each unique retailer will have all repeat payments added up
     DescAmount = defaultdict(float)
     for t in transactions:
             if t["Type"] == "Card Payment":
                     DescAmount[t["Description"]]-= t["Amount"]
     return DescAmount
     
#top 10 spending totals
def AllTime_top_10_dict(totals):
    #sorts the dict in reverse order(highest first) depending on the amount and limeted to 10 items total
    return dict(sorted(totals.items(), key=lambda item:item[1], reverse=True)[:10])

def monthly_spending(transactions):
    totals = defaultdict(float)
    for t in get_spending(transactions):
        #strftime turns time into text
        month = t["Started Date"].strftime("%Y-%m")
        totals[month] -= t["Amount"]
    return {month: round(total, 2) for month, total in sorted(totals.items())}
            

    

    

    
    



if __name__ == "__main__":
    data = parse_csv("data/private/trackerBankStatement.csv")
    #print("Net saved:", net_saved(data))
    #print("Net spent:", net_spent(data))
    #print("Net top-up:", net_topup(data))
    #print("top 10", top_10_spending(data))
    DescAmount = Descript_amount_dict(data)
    sorted_t10 = AllTime_top_10_dict(DescAmount)
    for retailer,total in sorted_t10.items():
        print(f"{retailer}: £{total:.2f}")

    monthly = monthly_spending(data)
    for month, total in monthly.items():
          print(f"{month}: £{total:.2f}")
    print(round(sum(monthly.values()), 2) == net_spent(data)) 


