import sqlite3 
from telegram import Update 
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters






# Инициализация базы данных
conn = sqlite3.connect('survey.db')
cursor = conn.cursor()

# Создание таблицы для хранения ответов
cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                  user_id INTEGER,
                  message TEXT)''')
conn.commit()

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    welcome_message = "Вітаємо! Це бот для опитування. Відправте вашу відповідь на запитання."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# Обработчик текстовых сообщений
def handle_text_message(update: Update, context: CallbackContext):
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Збереження відповіді в базі даних
    cursor.execute("INSERT INTO survey_responses (user_id, message) VALUES (?, ?)",
                   (user_id, message_text))
    conn.commit()
    
    reply_message = "Дякуємо! Ваша відповідь збережена."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    
    cursor.close()
    conn.close()

# Обработчик команды /responses
def view_responses(update: Update, context: CallbackContext):
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    
    # Запит всіх відповідей з бази даних
    cursor.execute("SELECT * FROM survey_responses")
    responses = cursor.fetchall()
    
    # Формування повідомлення з відповідями
    message = "Відповіді на опитування:\n\n"
    for response in responses:
        user_id, response_text = response[1], response[2]
        message += f"Користувач {user_id}: {response_text}\n"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    cursor.close()
    conn.close()

# Создание экземпляра Updater и регистрация обработчиков
TOKEN = '6006450262:AAH6jim5DwecaNe9xMv35nQUkSwnd8jzAWs'
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

text_message_handler = MessageHandler(None, handle_text_message)
dispatcher.add_handler(text_message_handler)

responses_handler = CommandHandler('responses', view_responses)
dispatcher.add_handler(responses_handler)

# Запуск бота
updater.start_polling()

# Остановка бота по нажатию Ctrl+C
updater.idle()
