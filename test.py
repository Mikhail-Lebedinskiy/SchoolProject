import telebot
import csv
import datetime
from GoogleSheets_parser import read_google_sheets
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


class Bot():

    def __init__(self):
        self.bot = telebot.TeleBot('1719851501:AAEy5lCcl6YVcs_pF1XYrD-q2zCVANdnMQ8')

    @self.bot.message_handler(commands=['start'])
    def start_message(message):
        # обработка комманды старт

        if message.from_user.id not in authorized_people_data_frame['user_id'].values:
            # регистрация нового пользователя
            add_markup(message, my_class_array)
        else:
            # просим выбрать одн из команд
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row(*bot_functionality)
            bot.send_message(message.chat.id, 'Привет! Чем могу помочь?', reply_markup=keyboard)