import telebot


bot = telebot.TeleBot('1719851501:AAEy5lCcl6YVcs_pF1XYrD-q2zCVANdnMQ8')



@bot.message_handler(func=lambda message: True)
def start_message(message):
    print('fsfdg')
    print(message.text)


bot.polling(none_stop=True)