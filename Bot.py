import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Глоссарий (термины и определения)
GLOSSARY = {
    "Бережливое производство": "Философия управления, направленная на устранение трёх видов потерь (муда, мури, мура). Цель — полное устранение действий, не добавляющих ценности.",
    "Муда": "Действия, не добавляющие ценности. 7 видов: перепроизводство, ожидание, транспортировка, излишняя обработка, запасы, лишние движения, брак.",
    "Мури": "Потери из-за перегрузки людей, процессов или оборудования.",
    "Мура": "Потери из-за неравномерности или нерегулярности процессов.",
    "Кайдзен": "Непрерывное совершенствование через устранение потерь. Делать больше с меньшими затратами.",
    "Канбан": "Визуальные карточки для сигнала о необходимости действий (заказ, производство).",
    "5S": "Система организации рабочего места: сортировка, порядок, чистота, стандартизация, совершенствование.",
    "TPM": "Всеобщий уход за оборудованием для достижения нулевых потерь.",
    "SMED": "Быстрая переналадка оборудования. Single-Minute Exchange of Die.",
    "Jidoka": "Автоматическая остановка оборудования при браке. Принцип автономизации.",
    "Just-in-time": "Производить только то, что нужно, в нужном количестве и к нужному сроку.",
    "PDCA": "Plan-Do-Check-Act — цикл непрерывного улучшения (Цикл Деминга).",
    "A3": "Решение проблем на одном листе формата A3 (11×17 дюймов).",
    "VSM": "Карта потока ценности для выявления потерь. Value Stream Mapping.",
    "Андон": "Визуальный контроль состояния процессов. Система сигналов.",
    "Пока-ёкэ": "Защита от дурака, предотвращение случайных ошибок. Poka-Yoke.",
    "Гемба": "Реальное место, где создаётся ценность (производственный цех, стройка).",
    "Хосин Канри": "Развёртывание политики и целей компании. Связь стратегии с исполнением.",
    "Обея": "Большая комната для командной работы и визуализации проектов. Obeya Room.",
    "Диаграмма спагетти": "Карта движения оператора для оптимизации путей и устранения лишних перемещений.",
}

# Функция, которая создаёт клавиатуру со всеми терминами
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

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="📚 *Глоссарий Leanwave*\n\nВыберите термин:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# Обработчик всех кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Если нажата кнопка "Оглавление"
    if data == "to_glossary":
        await query.edit_message_text(
            text="📚 *Глоссарий Leanwave*\n\nВыберите термин:",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    # Если нажат термин (начинается с "term_")
    elif data.startswith("term_"):
        term = data[5:]  # Убираем "term_" из начала
        definition = GLOSSARY.get(term, "❌ Определение не найдено.")
        
        # Клавиатура с кнопкой "Оглавление"
        keyboard = [[InlineKeyboardButton("📋 Оглавление", callback_data="to_glossary")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"📖 *{term}*\n\n{definition}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    # ⚠️ ЗАМЕНИТЕ НА ВАШ ТОКЕН (получите у @BotFather):
    TOKEN = "8816363608:AAHibmMH6QXgJVCpk4jnFAb-UH1JAEXCgzU"
    
    app = Application.builder().token(TOKEN).build()
    
    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Для PythonAnywhere используем Flask + webhook
    from flask import Flask, request
    flask_app = Flask(__name__)
    
    @flask_app.route('/webhook', methods=['POST'])
    async def webhook():
        await app.update_queue.put(Update.de_json(request.get_json(), app.bot))
        return 'ok'
    
    @flask_app.route('/')
    def index():
        return 'Бот работает!'
    
    flask_app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()