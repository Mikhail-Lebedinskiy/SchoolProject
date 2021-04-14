import telebot
import csv
import pandas as pd
import numpy as np
from keyboa import keyboa_maker
from pprint import pprint
import time
import datetime
import traceback
from GoogleSheets_parser import read_google_sheets
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

bot = telebot.TeleBot('1719851501:AAEy5lCcl6YVcs_pF1XYrD-q2zCVANdnMQ8')
authorized_people_data_frame = pd.DataFrame(columns=['name', 'surname', 'user_id', 'english_group', 'economic_group',
                                                     'physic_group', 'geometry_group', 'informatics_group'])
my_class_array = ['Бахышева Эмма', 'Григорьев Сева', 'Гультяев Андрей', 'Дударева Вика', 'Иго Пётр',
                  'Колесников Никита', 'Коляда Миша', 'Кузьмина Валя', 'Лебединский Миша', 'Лунёва Маша',
                  'Мышкина Валя', 'Огилько Дима', 'Опальчук Арина', 'Павлова Соня', 'Рябов Ян', 'Селиванов Захар',
                  'Сусленков Паша', 'Харитонов Алёша', 'Харьков Саша', 'Хроменко Юля', 'Чеблакова Алина',
                  'Чеботарева Аня', 'Шурин Сева', 'Яковлев Гриша']
bot_functionality = ['/View_Tomorrow', '/дз-по-предмету']
table_dict = {'Бахышева Эмма': ['0', '0', '0', '0', '0'], 'Григорьев Сева': ['0', '1', '1', '1', '1'],
              'Гультяев Андрей': ['1', '0', '0', '0', '0'], 'Дударева Вика': ['0', '0', '1', '1', '1'],
              'Иго Пётр': ['0', '1', '1', '1', '1'], 'Колесников Никита': ['0', '0', '0', '0', '0'],
              'Коляда Миша': ['0', '0', '0', '0', '0'], 'Кузьмина Валя': ['1', '1', '1', '1', '0'],
              'Лебединский Миша': ['1', '0', '1', '1', '1'], 'Лунёва Маша': ['0', '0', '0', '0', '1'],
              'Мышкина Валя': ['1', '0', '0', '0', '0'], 'Огилько Дима': ['1', '0', '1', '1', '0'],
              'Опальчук Арина': ['0', '0', '0', '0', '0'], 'Павлова Соня': ['1', '1', '1', '1', '0'],
              'Рябов Ян': ['0', '0', '1', '1', '0'], 'Селиванов Захар': ['0', '0', '1', '1', '0'],
              'Сусленков Паша': ['1', '0', '1', '1', '1'], 'Харитонов Алёша': ['1', '0', '1', '1', '0'],
              'Харьков Саша': ['1', '1', '1', '1', '1'], 'Хроменко Юля': ['0', '1', '1', '1', '1'],
              'Чеблакова Алина': ['0', '0', '0', '0', '1'], 'Чеботарева Аня': ['1', '1', '1', '1', '1'],
              'Шурин Сева': ['1', '0', '0', '0', '0'], 'Яковлев Гриша': ['0', '0', '1', '1', '1']}
subjects = read_google_sheets('A1:U1')
subjects_count = len(subjects)
subjects_with_groups = set(['Информатика', 'Английский', 'Экономика', 'Геометрия', 'Физика'])
from_subject_to_column = {'Английский': 3, 'Экономика': 4, 'Физика': 5, 'Геометрия': 6, 'Информатика': 7}


def create_calendar(message):
    # создаёт календарь для удобного выбора даты

    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


def call_calendar(call):
    # обработка введённой пользователем даты

    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              call.message.chat.id,
                              call.message.message_id)
        return result


def data_base_update(name, surname, user_id):
    # добавляет нового пользователя в базу данных

    with open('DATA/users_data_base.csv', 'a', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, surname, user_id, *table_dict[surname + ' ' + name]])


def data_frame_update(name, surname, user_id):
    # добавляет нового пользователя в датафрейм

    print([name, surname, user_id, *table_dict[surname + ' ' + name]])
    authorized_people_data_frame.loc[user_id] = [name, surname, user_id, *table_dict[surname + ' ' + name]]


def add_markup(message, markups):
    # выводит пользователю список отвтов

    markup = telebot.types.InlineKeyboardMarkup()
    for i in markups:
        markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
    bot.send_message(message.chat.id, 'Здарова, бродяга!')
    bot.send_message(message.chat.id, 'Напиши своё имя', reply_markup=markup)


def get_markup_answer(call):
    # преобразовывает ответ пользователя в дату

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
    bot.send_message(call.message.chat.id, call.data)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    return call.data


def new_user_authorization(message, user_id):
    # регистрация нового пользователя

    add_markup(message, my_class_array)

    @bot.callback_query_handler(func=lambda call: ' ' in call.data)
    def query_handler(call):
        print()
        print(type(call))
        surname, name = get_markup_answer(call).split()
        data_frame_update(name, surname, user_id)
        data_base_update(name, surname, user_id)


def get_homework(date, message):
    # возвращает ДЗ по дате

    row = date - datetime.datetime(2021, 4, 10)
    row = row.days + 2

    answer = {}
    homework = read_google_sheets(f'A{row}:U{row}')
    for i in range(len(homework)):
        if homework[i] == '':
            continue
        if subjects[i][:-1] in subjects_with_groups:
            if subjects[i][-1] == authorized_people_data_frame.loc[message.from_user.id]\
                    [from_subject_to_column[subjects[i][:-1]]]:
                answer[subjects[i][:-1]] = homework[i]
                continue
            else:
                continue
        answer[subjects[i]] = homework[i]
    return answer.copy()


@bot.message_handler(commands=['View_Day'])
def view_day(message):
    # обработка команды /View_Day

    create_calendar(message)

    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def call(c):
        # обрабатывает ответ пользователя

        date = call_calendar(c)
        answer = get_homework(date, message)
        homework_message = ''
        for key, value in answer.items():
            homework_message += key + '\t' + value + '\n'

        bot.send_message(message.chat.id, homework_message)


@bot.message_handler(commands=['View_Tomorrow'])
def homework_tomorrow(message):
    # обработка команды /View_Tomorrow

    date = datetime.datetime.now()
    one_days = datetime.timedelta(1)
    date = date + one_days
    answer = get_homework(date, message)
    homework_message = ''
    for key, value in answer.items():
        homework_message += key + '\t' + value + '\n'

    bot.send_message(message.chat.id, homework_message)


# start
@bot.message_handler(commands=['start'])
def start_message(message):
    # обработка комманды старт

    user_id = message.from_user.id
    if message.from_user.id not in authorized_people_data_frame['user_id'].values:
        # регистрация нового пользователя
        new_user_authorization(message, user_id)
    else:
        # просим выбрать одн из команд
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row(*bot_functionality)
        bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        traceback.print_exc()
        # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
