import telebot
from data import authorized_people_data_frame, my_class_array, bot_functionality, table_dict, subjects, subjects_count, \
    subjects_with_groups, from_subject_to_column
from data import data_frame_update, data_base_update
import datetime
from GoogleSheets_parser import read_google_sheets
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import traceback
import time


bot = telebot.TeleBot('1719851501:AAEy5lCcl6YVcs_pF1XYrD-q2zCVANdnMQ8')


# start
@bot.message_handler(commands=['start'])
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


def add_markup(message, markups):
    # выводит пользователю список отвтов

    markup = telebot.types.InlineKeyboardMarkup()
    for i in markups:
        markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
    bot.send_message(message.chat.id, 'Здарова, бродяга!')
    bot.send_message(message.chat.id, 'Напиши своё имя', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: ' ' in call.data)
def query_handler(call):
    # обрабатывает ответ пользователя

    surname, name = get_markup_answer(call).split()
    data_frame_update(name, surname, call.from_user.id)
    data_base_update(name, surname, call.from_user.id)


def get_markup_answer(call):
    # возвращает ответ пользователя

    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
    bot.send_message(call.message.chat.id, call.data)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    return call.data


@bot.message_handler(commands=['View_Tomorrow'])
def homework_tomorrow(message):
    # обработка команды /View_Tomorrow

    date = datetime.datetime.now()
    one_days = datetime.timedelta(1)
    date = date + one_days
    answer = get_homework(date.date(), message)
    send_homework(message.chat.id, answer)


def get_homework(date, message):
    # возвращает ДЗ по дате

    row = date - datetime.date(2021, 4, 10)
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


def send_homework(chat_id, homework):
    # отправляет сообщение с домашним заданием пользователю

    homework_message = ''
    for key, value in homework.items():
        homework_message += key + '\t' + value + '\n'

    bot.send_message(chat_id, homework_message)


@bot.message_handler(commands=['View_Day'])
def start(m):
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
        send_homework(call.message.chat.id, get_homework(result, call))


@bot.message_handler(func=lambda message: 'View_Next_' in message.text, content_types=['text'])
def View_Next_N(message):
    a = message.text.split('_')
    N = int(a[2])
    date = datetime.datetime.now()
    one_days = datetime.timedelta(1)
    date = date + one_days
    for i in range(N):
        answer = get_homework(date.date(), message)
        send_homework(message.chat.id, answer)
        date = date + one_days


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        traceback.print_exc()
        # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)