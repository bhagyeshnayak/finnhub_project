if __name__ == "__main__":
#     symbols_data = get_all_symbols()

#     print(f"Total symbols: {len(symbols_data)}")

#     all_companies = []

#     # Take first 50 (IMPORTANT - avoid rate limit)
#     for item in symbols_data[:50]:
#         symbol = item.get("symbol")

#         if not symbol:
#             continue

#         data = get_company_profile(symbol)

#         if data and data.get("name"):
#             all_companies.append(data)
#             print(f"Fetched: {symbol}")

#         time.sleep(1)  # avoid rate limit

#     # Save
#     with open("data/companies.json", "w", encoding="utf-8") as f:
#         json.dump(all_companies, f, indent=4, ensure_ascii=False)

#     print("✅ All company data saved")