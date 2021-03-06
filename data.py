from GoogleSheets_parser import read_google_sheets
import csv
import pandas as pd


def data_frame_update(name, surname, user_id):
    # добавляет нового пользователя в датафрейм

    print([name, surname, user_id, *table_dict[surname + ' ' + name]])
    authorized_people_data_frame.loc[user_id] = [name, surname, user_id, *table_dict[surname + ' ' + name]]


def data_base_update(name, surname, user_id):
    # добавляет нового пользователя в базу данных

    with open('DATA/users_data_base.csv', 'a', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, surname, user_id, *table_dict[surname + ' ' + name]])


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