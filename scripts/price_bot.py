import requests, os, time

TELEGRAM_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "8006453460")

def main():
    msg = "signal bot connecting..."
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price",
            params={"symbol": "BTCUSDT", "type": "MINI"},
            headers=headers,
            timeout=10,
        )
        print("status", r.status_code, "url", r.url)
        data = r.json()
        print("binance data", data)
        price = data.get("price") or data.get("lastPrice") or ""
        if price:
            ts = time.strftime("%H:%M UTC")
            msg = f"BTC Binance: ${price} {ts}"
        else:
            msg = f"no price in binance resp: {str(data)[:200]}"
    except Exception as e:
        msg = f"binance err: {e}"
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
    print(msg)

if __name__ == "__main__":
    main()
