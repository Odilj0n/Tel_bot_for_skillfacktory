import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, Curconverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = "Привет, я бот который показывает актуальные курсы валют. Чтобы продолжит " \
           "введи данные по форме: доллар рубль 100\n" \
           "\n" \
           "/values - список доступных валют\n" \
           "\n" \
           "/help - если что-то не понятно"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message):
    text = "Название валют нужно ввести в соответствии с /values - списком доступных валют." \
           "Обрати внимание, что сумму в валюте нужно указывать без запятых\n" \
           "(Можно использовать точку)" \
           "\nПример: доллар рубль 100.5" \
           "\n" \
           "\n/start - Обратно в начало" \
           "\n" \
           "\n/values - Список доступных валют"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionExeption("Что-то тут не так, попробуй еще раз.")

        quote, base, amount = values
        total_base = Curconverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Видимо ты где-то ошибся,\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Извини,{e} нет в списке доступных мной валют\n")
    else:
        text = f"Цена {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)
