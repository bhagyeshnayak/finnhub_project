import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from flask import Flask, render_template, request

from config.settings import API_KEY, BASE_URL


app = Flask(__name__)

DATA_FILE = Path(__file__).resolve().parent / "data" / "companies.json"


def load_companies():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            companies = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    valid_companies = [company for company in companies if company.get("ticker")]
    return sorted(valid_companies, key=lambda company: company["ticker"])


def get_stock_quote(symbol):
    if not API_KEY:
        return None

    query = urlencode({"symbol": symbol, "token": API_KEY})
    url = f"{BASE_URL}/quote?{query}"

    try:
        with urlopen(url, timeout=10) as response:
            if response.status == 200:
                return json.load(response)
    except OSError:
        return None

    return None


@app.route("/", methods=["GET", "POST"])
def home():
    companies = load_companies()
    company_data = None
    quote_data = None
    symbol = ""

    if request.method == "POST":
        symbol = request.form.get("symbol", "").strip().upper()

        if symbol:
            company_data = next(
                (company for company in companies if company.get("ticker") == symbol),
                None,
            )
            quote_data = get_stock_quote(symbol)

    return render_template(
        "index.html",
        companies=companies,
        company_data=company_data,
        quote_data=quote_data,
        symbol=symbol,
        api_configured=bool(API_KEY),
    )


if __name__ == "__main__":
    app.run(debug=True)
