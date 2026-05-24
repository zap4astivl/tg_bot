import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Настройка логирования (чтобы видеть ошибки в облаке)
logging.basicConfig(level=logging.INFO)

# Токен бота берем из переменных окружения (так безопаснее)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Функция для команды /start
async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Добрый день!\n"
        "Отправьте VIN автомобиля (17 символов), и я сохраню его."
    )

# Функция для обработки VIN-номера
async def handle_vin(update: Update, context):
    user_vin = update.message.text.strip().upper()
    user_id = update.effective_user.id
    username = update.effective_user.username or "без_username"
    
    # Простая проверка: VIN должен быть 17 символов
    if len(user_vin) == 17:
        # Сохраняем в файл (на Render файлы хранятся временно, но для начала хватит)
        with open("clients.txt", "a", encoding="utf-8") as f:
            f.write(f"ID: {user_id}, Username: @{username}, VIN: {user_vin}\n")
        
        await update.message.reply_text(
            f"✅ Спасибо! VIN {user_vin} принят.\n"
            "Наш менеджер свяжется с вами в ближайшее время."
        )
    else:
        await update.message.reply_text(
            "❌ VIN номер должен состоять из 17 символов.\n"
            "Пожалуйста, проверьте и отправьте снова.\n"
        )

# Главная функция
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vin))
    
    logging.info("Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()