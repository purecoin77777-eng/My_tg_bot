import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

GLOSSARY = {
    "Бережливое производство": "Философия управления, направленная на устранение трёх видов потерь (муда, мури, мура). Цель — полное устранение действий, не добавляющих ценности.",
    "Муда": "Действия, не добавляющие ценности. 7 видов: перепроизводство, ожидание, транспортировка, излишняя обработка, запасы, лишние движения, брак.",
    "Мури": "Потери из-за перегрузки людей, процессов или оборудования.",
    "Мура": "Потери из-за неравномерности процессов.",
    "Кайдзен": "Непрерывное совершенствование через устранение потерь.",
    "Канбан": "Визуальные карточки-сигналы.",
    "5S": "Сортировка, порядок, чистота, стандартизация, совершенствование.",
    "TPM": "Всеобщий уход за оборудованием.",
    "SMED": "Быстрая переналадка.",
    "Jidoka": "Автоматическая остановка при браке.",
    "Just-in-time": "Производить только то, что нужно, когда нужно.",
    "PDCA": "Plan-Do-Check-Act — цикл улучшений.",
    "A3": "Решение проблем на одном листе.",
    "VSM": "Карта потока ценности.",
    "Андон": "Визуальный контроль состояния.",
    "Пока-ёкэ": "Защита от дурака.",
    "Гемба": "Реальное место создания ценности.",
    "Хосин Канри": "Развёртывание политики компании.",
    "Обея": "Большая комната для команд.",
    "Диаграмма спагетти": "Карта движений оператора.",
}

def get_main_keyboard():
    keyboard = []
    terms = list(GLOSSARY.keys())
    for i in range(0, len(terms), 2):
        row = []
        row.append(InlineKeyboardButton(terms[i], callback_data=f"term_{terms[i]}"))
        if i + 1 < len(terms):
            row.append(InlineKeyboardButton(terms[i + 1], callback_data=f"term_{terms[i + 1]}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="📚 *Глоссарий Leanwave*\n\nВыберите термин:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "to_glossary":
        await query.edit_message_text(
            text="📚 *Глоссарий Leanwave*\n\nВыберите термин:",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    elif data.startswith("term_"):
        term = data[5:]
        definition = GLOSSARY.get(term, "❌ Определение не найдено.")
        keyboard = [[InlineKeyboardButton("📋 Оглавление", callback_data="to_glossary")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"📖 *{term}*\n\n{definition}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    TOKEN = os.environ.get("TOKEN")  # берём токен из переменных окружения на Bothost
    if not TOKEN:
        raise ValueError("Токен не найден! Установите переменную TOKEN на Bothost.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Бот запущен в режиме polling (без webhook)")
    app.run_polling()

if __name__ == "__main__":
    main()
