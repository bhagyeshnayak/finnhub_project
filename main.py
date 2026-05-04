import json
import time
from services.finnhub_service import get_all_symbols, get_company_profile
symbols_data = get_all_symbols()
print(f"Total symbols: {len(symbols_data)}")


with open("data/companie_symbols.json", "w", encoding="utf-8") as f:
    json.dump(symbols_data, f, indent=4, ensure_ascii=False)

#     all_companies = []
#     seen = set()

# for item in symbols_data:
#     if len(all_companies) >= 100:
#         break

#     symbol = item.get("symbol")

#     if not symbol or symbol in seen:
#         continue

#     data = get_company_profile(symbol)

#     if data and data.get("name"):
#         all_companies.append(data)
#         seen.add(symbol)
#         print(f"Fetched: {symbol}")

#     time.sleep(1)

# with open("data/companies.json", "w", encoding="utf-8") as f:
#     json.dump(all_companies, f, indent=4, ensure_ascii=False)

print("100 company data saved")

import json
from repository.company_repo import insert_company
from database.init_db import init_database

if __name__ == "__main__":
    # Initialize database and create tables
    init_database()

    # Load JSON
    with open("data/companies.json", "r", encoding="utf-8") as f:
        companies = json.load(f)

    print(f"Total companies in JSON: {len(companies)}")

    for company in companies:
        insert_company(company)
        print(f"Inserted: {company.get('ticker')}")

    print("\n Data inserted into MySQL successfully")