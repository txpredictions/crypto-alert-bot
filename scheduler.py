import asyncio
import os
from app.alerts import load_alerts, save_alerts
from app.prices import get_price

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

async def alert_checker(bot):
    while True:
        alerts = load_alerts()
        updated = False

        for user_id, coins in list(alerts.items()):
            for coin, target in list(coins.items()):
                price = get_price(coin)
                if price and price >= target:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"🚨 {coin.upper()} reached ${price}"
                    )
                    del alerts[user_id][coin]
                    updated = True

        if updated:
            save_alerts(alerts)

        await asyncio.sleep(CHECK_INTERVAL)
