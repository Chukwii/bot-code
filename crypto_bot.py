from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = "7927780147:AAGHSUkM1mlYVsDSCLbY_4HV8o40Jtsy0dw"
application = Application.builder().token(TOKEN).build()

# Function to get price from CoinGecko
def get_coingecko_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data[symbol]['usd']) if symbol in data else None

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Send a cryptocurrency symbol (e.g., bitcoin) to get price information.")

# Command to track crypto prices
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    crypto_symbol = update.message.text.lower()  # Get the symbol from the user's message

    # Get price from CoinGecko
    coingecko_price = get_coingecko_price(crypto_symbol)

    # Respond to the user
    if coingecko_price is not None:
        response = (
            f"CoinGecko Price for {crypto_symbol}: ${coingecko_price:.2f}\n"
        )
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Error fetching prices. Please check the cryptocurrency symbol.")

# Adding handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track))

# Run the bot
application.run_polling()
