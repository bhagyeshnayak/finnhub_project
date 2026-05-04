import requests
from config.settings import API_KEY, BASE_URL


def get_all_symbols():
    url = f"{BASE_URL}/stock/symbol"

    params = {
        "exchange": "US",
        "token": API_KEY
    }

    response = requests.get(url, params=params)

    print(f"Symbols API status: {response}")

    if response.status_code == 200:
        return response.json()

    return []


def get_company_profile(symbol):
    url = f"{BASE_URL}/stock/profile2"

    params = {
        "symbol": symbol,
        "token": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        print("Error:", e)

    return None