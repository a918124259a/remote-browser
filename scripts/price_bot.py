import requests, os, time, json

TELEGRAM_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "8006453460")

def main():
    msg = "signal bot test"
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
        price = r.json()["price"]
        ts = time.strftime("%H:%M UTC")
        msg = f"BTC Binance: ${price} {ts}"
    except Exception as e:
        msg = f"binance err: {e}"
    if TELEGRAM_BOT:
        try:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
                          json={"chat_id": TELEGRAM_CHAT, "text": msg},
                          timeout=10)
        except Exception as e:
            msg += f" tg_err: {e}"
    print(msg)

if __name__ == "__main__":
    main()
