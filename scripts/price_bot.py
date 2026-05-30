import requests, os, time

TELEGRAM_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "8006453460")

def main():
    msg = "connecting..."
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"},
            headers=headers,
            timeout=15,
        )
        print("status", r.status_code)
        data = r.json()
        print("cg data", data)
        btc = data.get("bitcoin", {})
        price = btc.get("usd", "")
        chg = btc.get("usd_24h_change", "")
        if price:
            ts = time.strftime("%H:%M UTC")
            msg = f"BTC ${price:,.0f} ({chg:+.2f}%) {ts}"
        else:
            msg = f"no price: {str(data)[:200]}"
    except Exception as e:
        msg = f"err: {e}"
        print(msg)
    if TELEGRAM_BOT:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT, "text": msg},
                timeout=10,
            )
        except Exception as e:
            print("tg_err", e)
    print("msg:", msg)

if __name__ == "__main__":
    main()
