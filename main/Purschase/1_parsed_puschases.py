from bs4 import BeautifulSoup
from collections import defaultdict
import json

# Load the HTML content
html_path = r"..\..\Data\Purchase\history.html "

with open(html_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Constants
usd_to_tl_rate = 35

# Parse the purchase table
rows = soup.select(".wallet_history_table .wallet_table_row")
purchases_by_date = defaultdict(lambda: {"number of purchased games in that date": 0, "total cost": 0.0})

for row in rows:
    # Extract data from the row
    date = row.select_one(".wht_date").text.strip()
    item_type = row.select_one(".wht_type > div").text.strip()
    total_cost_text = row.select_one(".wht_total").text.strip()

    # Skip non-game purchases
    if item_type in ["Oyun İçi Satın Alım", "Pazar İşlemi"]:
        continue

    try:
        # Clean the total cost string
        if "USD" in total_cost_text:
            total_cost = float(total_cost_text.replace("$", "").replace("USD", "").strip()) * usd_to_tl_rate
        elif "TL" in total_cost_text:
            total_cost = float(total_cost_text.split()[0].replace(",", ".").strip())
        else:
            # Skip rows with unexpected formats
            continue
    except ValueError:
        # Skip rows with invalid total cost formats
        print(f"Skipping row with invalid total cost: {total_cost_text}")
        continue

    # Update purchases data
    purchases_by_date[date]["number of purchased games in that date"] += 1
    purchases_by_date[date]["total cost"] += total_cost

# Convert results to the desired format
formatted_purchases = []
for date, data in purchases_by_date.items():
    formatted_purchases.append({
        "date": date,
        **data,
        "total cost": f"{data['total cost']:.2f} TL"
    })

# Output the results
with open("../../Data/Purchase/parsed_purchases.json", "w", encoding="utf-8") as output_file:
    json.dump(formatted_purchases, output_file, ensure_ascii=False, indent=4)

print(f"Parsed purchases saved as parsed_purchases.json")
