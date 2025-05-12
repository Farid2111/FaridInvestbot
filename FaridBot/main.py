
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

assets = [
    {"ticker": "FXTB", "desc": "ETF на короткие ОФЗ — 3 лота"},
    {"ticker": "SBER", "desc": "Сбербанк — 3 шт."},
    {"ticker": "TCSG", "desc": "Тинькофф Групп — 1 шт."},
    {"ticker": "FXRL", "desc": "ETF на индекс МосБиржи — 2 лота"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "**Покупка на этой неделе**\n\n"
    for a in assets:
        message += f"• `{a['ticker']}` — {a['desc']}\n"
    keyboard = [
        [InlineKeyboardButton("✅ Купить", callback_data="buy"),
         InlineKeyboardButton("⏳ Отложить", callback_data="later")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy":
        await query.edit_message_text("Зайди в приложение Альфа-Инвестиции и купи:\n\n" +
            "\n".join([f"- {a['desc']}" for a in assets]) + "\n\nПосле покупки — нажми /start на следующей неделе.")
    elif query.data == "later":
        await query.edit_message_text("Окей, напомню позже. Напиши /start, когда будешь готов.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
