from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

import os

TOKEN = '7169303851:AAEWZX2pwZtLdsduVGagwJv04kHMQMoUheI'
ADMIN_CHAT_ID = 7039411923

# Флаг ожидания заявки
WAITING_FOR_FORM = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 /start вызван")
    keyboard = [
        [InlineKeyboardButton("Оставить заявку", callback_data='zayavka')],
        [InlineKeyboardButton("Информация", callback_data='info')],
        [InlineKeyboardButton("Связаться с нами", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Это EXCHANGEBOT, оставь свою заявку и мы свяжемся с тобой!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    print(f"🔘 Нажата кнопка: {query.data}")

    if query.data == 'zayavka':
        WAITING_FOR_FORM[user_id] = True
        await query.message.edit_text(
            "Пожалуйста, заполните форму:\n\n"
            "1. Сумма:\n"
            "2. Имя:\n"
            "3. Банк отправителя:\n"
            "4. Банк получателя:\n"
            "5. *Если операция с криптовалютой:*\n"
            "**Валютные пары (например, USDT -> BTC):**",
            parse_mode='Markdown'
        )

    elif query.data == 'info':
        await query.message.reply_text(
            "**Сервис обмена валют и переводов по всему миру**\n\n"
            "Мы работаем с большинством валютных пар и банками мира.\n"
            "Минимальная сумма — от $500.",
            parse_mode='Markdown'
        )

    elif query.data == 'contact':
        await query.message.reply_text("Связаться с нами: @bitcoinexchangebiz")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text

    if WAITING_FOR_FORM.get(user_id):
        print("✅ Заявка получена от пользователя")
        WAITING_FOR_FORM[user_id] = False

        msg = f"📩 Новая заявка от @{user.username or user.first_name} (ID: {user.id}):\n\n{text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
        await update.message.reply_text("✅ Спасибо! Ваша заявка отправлена.")

        # Показываем меню снова
        await start(update, context)

    else:
        await update.message.reply_text("Напишите /start для начала.")

if __name__ == '__main__':
    print("🗂️ Запущен файл:", os.path.abspath(__file__))

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Бот запущен без ошибок и предупреждений.")
    app.run_polling()
