import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from dotenv import load_dotenv

from app.prices import get_price
from app.alerts import add_alert, load_alerts, delete_alert
from app.scheduler import alert_checker

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Crypto Alert Bot\n\n"
        "/price BTC\n"
        "/alert BTC 65000\n"
        "/myalerts\n"
        "/delete BTC"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = context.args[0].lower()
    price = get_price(coin)
    if price:
        await update.message.reply_text(f"{coin.upper()} price: ${price}")
    else:
        await update.message.reply_text("Coin not found ❌")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = context.args[0].lower()
    target = float(context.args[1])
    add_alert(update.effective_user.id, coin, target)
    await update.message.reply_text(f"✅ Alert set for {coin.upper()} at ${target}")

async def myalerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alerts = load_alerts().get(str(update.effective_user.id), {})
    if not alerts:
        await update.message.reply_text("No active alerts.")
        return
    msg = "\n".join([f"{c.upper()} → ${t}" for c, t in alerts.items()])
    await update.message.reply_text(msg)

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = context.args[0].lower()
    delete_alert(update.effective_user.id, coin)
    await update.message.reply_text(f"🗑️ Deleted alert for {coin.upper()}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("myalerts", myalerts))
    app.add_handler(CommandHandler("delete", delete))

    asyncio.create_task(alert_checker(app.bot))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
