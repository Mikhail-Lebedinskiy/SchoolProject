from pprint import pprint
import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import csv
import traceback
import time


bot = telebot.TeleBot('1719851501:AAEy5lCcl6YVcs_pF1XYrD-q2zCVANdnMQ8')
my_class_array = ['Бахышева Эмма', 'Григорьев Сева', 'Гультяев Андрей', 'Дударева Вика', 'Иго Пётр',
                  'Колесников Никита', 'Коляда Миша', 'Кузьмина Валя', 'Лебединский Миша', 'Лунёва Маша',
                  'Мышкина Валя', 'Огилько Дима', 'Опальчук Арина', 'Павлова Соня', 'Рябов Ян', 'Селиванов Захар',
                  'Сусленков Паша', 'Харитонов Алёша', 'Харьков Саша', 'Хроменко Юля', 'Чеблакова Алина',
                  'Чеботарева Аня', 'Шурин Сева', 'Яковлев Гриша']
bot_functionality = ['/View_Tomorrow', '/View_Day']


class GoogleSheetsParser():

    def __init__(self, credentials_file, spreadsheet_id):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.subjects = ['Дата', 'География', 'Русский', 'Литература', 'Алгебра', 'Геометрия0', 'Геометрия1', 'Физика0',
                         'Физика1', 'Информатика0', 'Информатика1', 'Английский0', 'Английский1', 'Экономика0',
                         'Экономика1', 'История', 'Обществознание', 'ОБЖ', 'Биология', 'Химия', 'Физ-ра']
        self.subjects_with_groups = set(['Информатика', 'Английский', 'Экономика', 'Геометрия', 'Физика'])
        self.from_subject_to_column = {'География': 'B', 'Русский': 'C', 'Литература': 'D', 'Алгебра': 'E',
                                       'Геометрия0': 'F', 'Геометрия1': 'G', 'Физика0': 'H', 'Физика1': 'I',
                                       'Информатика0': 'J', 'Информатика1': 'K', 'Английский0': 'L', 'Английский1': 'M',
                                       'Экономика0': 'N', 'Экономика1': 'O', 'История': 'P', 'Обществознание': 'Q',
                                       'ОБЖ': 'R', 'Биология': 'S', 'Химия': 'T', 'Физ-ра': 'U'}

    def from_homeworkArray_to_homeworkDict(self, homework_array, user):
        answer = {}
        for i in range(len(homework_array)):
            if homework_array[i] == '':
                continue
            if self.subjects[i][:-1] in self.subjects_with_groups:
                if self.subjects[i][-1] == user.group_dict[self.subjects[i][:-1]]:
                    answer[slf.subjects[i][:-1]] = homework[i]
                    continue
                else:
                    continue
            answer[self.subjects[i]] = homework_array[i]
        return answer.copy()

    def from_day_to_row(self, day_date):
        row = day_date - datetime.date(2021, 4, 10)  # вычитаем из данной даты дату первой строки.
        row = row.days + 2  # пребавляем 2 т.к. певый день на второй строке
        return row

    def get_homework_for_selected_day(self, day_date, user, column_range='AU'):
        row = self.from_day_to_row(day_date)
        range = column_range[0] + str(row) + ':' + column_range[1] + str(row)
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range,
            majorDimension='ROWS'
        ).execute()
        return self.from_homeworkArray_to_homeworkDict(values['values'][0], user)  # в values лежит двумерный список из одного элементы поэтому берём нулевой элемент

    def get_homework_for_selected_period_days(self, start_day_date, end_day_date, user):
        homework = []
        present_day_date = start_day_date

        # в цикле поочерёдно перебираем дни, я и дз за каждый день добавляем в homework
        while present_day_date != end_day_date:
            homework.append(self.get_homework_for_selected_day(present_day_date))
            present_day_date = present_day_date + datetime.timedelta(1)
        return homework

    def get_homework_for_select_subject_and_day(self, day_date, subject, user):
        return self.get_homework_for_selected_day(day_date, self.from_subject_to_column[subject]*2)


class User():

    def __init__(self, user_id, chat_id, name, surname, group_dict):
        self.user_id = user_id
        self.chat_id = chat_id
        self.name = name
        self.surname = surname
        self.group_dict = group_dict
        # self.df =

    def mark_homework_as_done(self, day_date, subject):
        pass

    def get_current_status_homework_day(self, day):
        pass


class Bot():

    def send_homework_day(self, homework, user, bot):
        homework_message = ''
        for key, value in homework.items():
            homework_message += key + '\t' + value + '\n'

        bot.send_message(user.chat_id, homework_message)

    def send_homework_for_period_days(self, homework, user, bot):
        for i in homework:
            self.send_homework_day(i, user, bot)

    def add_markup(self, markups, chat_id, bot):
        # выводит пользователю список отвтов

        markup = telebot.types.InlineKeyboardMarkup()
        for i in markups:
            markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
        bot.send_message(chat_id, 'Здарова, бродяга!')
        bot.send_message(chat_id, 'Напиши своё имя', reply_markup=markup)


parser = GoogleSheetsParser('Project-99f7721baf37.json', '1walrfWQ65rxYF7dArX1HNOYYx9ROMo18jnK9NP2CRn0')
users_dict = {}
telegram_bot = Bot()


@bot.message_handler(commands=['View_Tomorrow'])
def homework_tomorrow(message):
    # обработка команды /View_Tomorrow

    date = datetime.datetime.now()
    date = date + datetime.timedelta(1)
    answer = parser.get_homework_for_selected_day(date.date(), users_dict[message.from_user.id])
    telegram_bot.send_homework_day(answer, users_dict[message.from_user.id], bot)


@bot.message_handler(commands=['View_Day'])
def view_day(m):
    print(m)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def call(call):
    print(call)
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
        print(result)
        telegram_bot.send_homework_day(parser.get_homework_for_selected_day(result, users_dict[call.from_user.id]),
                                  users_dict[call.from_user.id], bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    # обработка комманды старт

    if message.from_user.id not in users_dict.keys():
        # регистрация нового пользователя
        telegram_bot.add_markup(my_class_array, message.chat.id, bot)
    else:
        # просим выбрать одн из команд
        print(users_dict[message.from_user.id].group_dict)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row(*bot_functionality)
        bot.send_message(message.chat.id, 'Привет! Чем могу помочь?', reply_markup=keyboard)


def get_group_dict(name, surname):
    with open('Students.csv', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        headers = next(reader)
        print(headers)
        headers = headers[2:5] + ['Геометрия'] + headers[5:]
        print(headers)
        for row in reader:
            if row[0] == surname and row[1] == name:
                values = row[2:5] + row[4:5] + row[5:]
                return dict(zip(headers, values))


def data_base_update(name, surname, user_id):
    # добавляет нового пользователя в базу данных

    with open('DATA/users_data_base.csv', 'w', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, surname, user_id])


@bot.callback_query_handler(func=lambda call: ' ' in call.data)
def query_handler(call):
    # обрабатывает ответ пользователя

    bot.send_message(call.message.chat.id, call.data)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    surname, name = call.data.split()
    group_dict = get_group_dict(name, surname)
    users_dict[call.from_user.id] = User(call.from_user.id, call.message.chat.id, name, surname, group_dict)
    data_base_update(name, surname, call.from_user.id)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        traceback.print_exc()
        # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
