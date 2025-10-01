import telebot
from telebot import types
import random
import time
import threading

TOKEN = "8330762842:AAH47wYcnhkKEPItrqSEStNnqFPE5EFet0c"
bot = telebot.TeleBot(TOKEN)

MSG_FILE = "messages.txt"
CHAT_FILE = "chats.txt"

BOT_NAME = "амиго"


# --------------------- УТИЛИТЫ ---------------------

def save_message(text):
    """Сохраняем сообщение в базу"""
    with open(MSG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def get_all_messages():
    """Загружаем все сохранённые сообщения"""
    try:
        with open(MSG_FILE, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


def save_chat(chat_id):
    """Сохраняем чат"""
    chats = get_all_chats()
    if chat_id not in chats:
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(str(chat_id) + "\n")


def get_all_chats():
    """Загружаем список чатов"""
    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return [int(x) for x in f.read().splitlines()]
    except FileNotFoundError:
        return []


# --------------------- ШУТКИ ---------------------

JOKES = [
    "Почему программисты не любят природу? Слишком много багов 🐞",
    "Амиго всегда онлайн. Даже когда спит 😴",
    "Если бот упал — значит, он просто лёг отдохнуть 😂",
 "рома свинья", "полина шлюха", "влад ты сосал?", "жора трахал еву", "Аня отсоси владу", "угашенный привет",
"полина сделай слюнявый роме", "Полина тише", "Влад аня тебя любит",]


def get_random_joke():
    return random.choice(JOKES)


# --------------------- ОБРАБОТЧИКИ ---------------------

@bot.message_handler(commands=['start'])
def start_message(message):
    """Приветственное меню"""
    markup = types.InlineKeyboardMarkup()
    add_button = types.InlineKeyboardButton("➕ Добавить в группу", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    support_button = types.InlineKeyboardButton("📩 Поддержка", url="https://t.me/am1goz")
    markup.add(add_button)
    markup.add(support_button)

    bot.send_message(message.chat.id,
                     "👋 Привет! Я *Амиго* — бот, который шутит лучге твоего бывшего! 😎",
                     parse_mode="Markdown",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Сохраняем все сообщения и реагируем на имя"""
    if message.text:
        text = message.text.strip()
        save_message(text)
        save_chat(message.chat.id)

        # Если упомянули "Амиго"
        if BOT_NAME.lower() in text.lower():
            # 1 из 5 раз шутка, иначе фраза из базы
            if random.randint(1, 5) == 1:
                reply = get_random_joke()
            else:
                messages = get_all_messages()
                reply = random.choice(messages) if messages else "Я ещё ничего не знаю 🤔"
            bot.reply_to(message, reply)


# --------------------- БОЛТАЛКА ---------------------

def spam_random_messages():
    """Бот периодически пишет во все чаты"""
    while True:
        time.sleep(random.randint(30, 70))  # 1.5 - 4 мин
        messages = get_all_messages()
        chats = get_all_chats()
        if messages and chats:
            # 1 из 7 сообщений будет шуткой
            if random.randint(1, 7) == 1:
                msg = get_random_joke()
            else:
                msg = random.choice(messages)

            for chat in chats:
                try:
                    bot.send_message(chat, msg)
                except Exception as e:
                    print(f"Ошибка при отправке в {chat}:", e)


# --------------------- ЗАПУСК ---------------------

threading.Thread(target=spam_random_messages, daemon=True).start()
print("Бот 'Амиго' запущен!")
bot.infinity_polling()