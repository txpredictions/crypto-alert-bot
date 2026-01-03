import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_price(coin: str) -> float | None:
    try:
        response = requests.get(
            COINGECKO_URL,
            params={"ids": coin, "vs_currencies": "usd"},
            timeout=10
        )
        data = response.json()
        return data[coin]["usd"]
    except Exception:
        return None
