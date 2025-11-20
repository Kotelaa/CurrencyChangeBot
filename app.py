import telebot

from config import TOKEN, KEYS
from utils import ConvertionException, Convertion

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    """Handler for the /start and /help commands."""
    bot_instr = ("Для начала работы бота введите команду в следующем **формате**:\n\n"
                 "**<название валюты> <в какую валюту перевести> <сумма перевода>** \n\n"
                 "Например: доллар евро 500 \n"
                 "(Узнать, сколько 500 долларов в евро) \n\n"
                 "**Список всех доступных валют можно получить по команде** /values"
                 )
    bot.reply_to(message, bot_instr, parse_mode="Markdown")


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    """Handler for the /values command."""
    values_message = "Допустимые валюты для конвертации: "
    for key in KEYS.keys():
        values_message += f"\n· {key.capitalize()}"
    bot.reply_to(message, values_message)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    """Handler for the /convert command."""
    try:
        user_message = message.text.lower()

        for key in KEYS.keys():
            if " " in key:
                user_message = user_message.replace(key, key.replace(" ", "_"))

        # dollar euro 500  /  Сколько стоит евро в 500 долларах?
        parts_message = user_message.split()
        base, currency_change, amount = parts_message
        if len(parts_message) != 3:
            raise ConnectionError ("Неправильное колличество параметров! "
                  "Введите в формате: <название валюты> <в какую валюту перевести> <сумма перевода>")
        base = base.replace("_", " ")
        currency_change = currency_change.replace("_", " ")

        exchange_rate = Convertion.convert(base, currency_change, amount)

    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя {e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду: \n {e}")

    else:
        bot_reply = (f"Цена {amount} {KEYS[currency_change]} "
                     f"= {exchange_rate:.2f} {KEYS[base]}")
        bot.send_message(message.chat.id, bot_reply)



bot.polling(True)