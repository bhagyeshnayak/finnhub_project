import json
import time
from services.finnhub_service import get_all_symbols, get_company_profile
from repository.company_repo import insert_company
from database.init_db import init_database


def fetch_and_save_companies():
    print("\n🔹 STEP 1: Fetching symbols from Finnhub API...")

    symbols_data = get_all_symbols()
    print(f"✅ Total symbols fetched: {len(symbols_data)}")

    # Save raw symbols (optional)
    print("💾 Saving raw symbols to file...")
    with open("data/companie_symbols.json", "w", encoding="utf-8") as f:
        json.dump(symbols_data, f, indent=4, ensure_ascii=False)
    print("✅ Raw symbols saved successfully")

    print("\n🔹 STEP 2: Fetching company profiles...")

    all_companies = []
    seen = set()

    for index, item in enumerate(symbols_data, start=1):
        if len(all_companies) >= 100:
            print("\n🎯 Reached 100 companies limit")
            break

        symbol = item.get("symbol")
        mic = item.get("mic")

        if not symbol:
            print(f"⚠️ Skipping invalid entry at index {index}")
            continue

        if symbol in seen:
            print(f"⚠️ Duplicate symbol skipped: {symbol}")
            continue

        print(f"🔍 Fetching [{index}] Symbol: {symbol} | MIC: {mic}")

        try:
            profile = get_company_profile(symbol)

            if profile and profile.get("name"):
                profile["mic"] = mic
                all_companies.append(profile)
                seen.add(symbol)

                print(f"✅ Added: {symbol} ({profile.get('name')})")
            else:
                print(f"❌ No valid profile for: {symbol}")

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")

        time.sleep(1)  # rate limit safety

    print("\n💾 Saving company data to JSON...")

    with open("data/companies.json", "w", encoding="utf-8") as f:
        json.dump(all_companies, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved {len(all_companies)} companies to companies.json")


def insert_into_db():
    print("\n🔹 STEP 3: Initializing database...")

    init_database()
    print("✅ Database initialized")

    print("\n🔹 STEP 4: Loading company data from JSON...")

    try:
        with open("data/companies.json", "r", encoding="utf-8") as f:
            companies = json.load(f)

        print(f"✅ Total companies loaded: {len(companies)}")

    except FileNotFoundError:
        print("❌ ERROR: companies.json file not found")
        return

    print("\n🔹 STEP 5: Inserting data into database...")

    success_count = 0

    for index, company in enumerate(companies, start=1):
        if not company:
            print(f"⚠️ Skipping empty record at index {index}")
            continue

        try:
            insert_company(company)
            success_count += 1

            print(f"✅ [{index}] Inserted: {company.get('symbol')}")

        except Exception as e:
            print(f"❌ [{index}] Failed to insert {company.get('symbol')}: {e}")

    print("\n🎉 Database Insertion Complete")
    print(f"✅ Successfully inserted: {success_count} records")
    print(f"⚠️ Failed: {len(companies) - success_count} records")


if __name__ == "__main__":
    print("🚀 STARTING DATA PIPELINE")

    fetch_and_save_companies()

    insert_into_db()

    print("\n🏁 PIPELINE COMPLETED SUCCESSFULLY")