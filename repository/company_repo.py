from database.db_connection import connect_db


def insert_company(data):
    conn = connect_db()
    cursor = conn.cursor()

    try:
         # add mic and USD currency 
        currency = data.get("currency")
        if currency != "USD":
            print(f"Skipping {data.get('ticker')} (currency={currency})")
            return

        symbol = data.get("symbol") or data.get("ticker")
        name = data.get("name") or data.get("description") or symbol
        mic = data.get("mic")  # now will be available

        cursor.execute("""
        INSERT IGNORE INTO companies
        (name, ticker, symbol, country, industry, market_cap, currency, mic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name,
            symbol,  # ticker
            symbol,  # symbol
            data.get("country"),
            data.get("finnhubIndustry") or "N/A",
            data.get("marketCapitalization") or 0,
            currency,
            mic
        ))

        conn.commit()
        print(f"Inserted: {symbol} | MIC: {mic}")

    except Exception as e:
        print("Error inserting:", data.get("ticker"), e)

    finally:
        cursor.close()
        conn.close()