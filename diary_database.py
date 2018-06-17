import sqlite3

conn = sqlite3.connect("data_for_diary.db")  # создание связи с базой данных
cursor = conn.cursor()  # обьект, позволящий взаимодействовать с базой данных, добавлять записи и т. д.

cursor.execute('''CREATE TABLE diary_events
                (event_title text, event_time text)''')
# создание таблицы: event_title - название события, event_time - время события


def get_connect():
    return conn


def update_record(new_title, new_time):  # возможно сюда можно будет пихнуть значения по умолчанию
    sql = '''UPDATE diary_events
            ...'''
    cursor.execute(sql)
    conn.commit()


def delete_record(title, time):
    sql = '''DELETE FROM diary_events WHERE ...'''
    cursor.execute(sql)
    conn.commit()


def add_record(add_title, add_time):
    sql = '''INSERT INTO diary_events VALUES(?)''', tuple(add_title, add_time)
    cursor.execute(sql)
    conn.commit()
# нужно добавить функции:
# редактирования записи
# удаления записи
# добавления записи (название + время (дата + часы), время(дата) + (без заголовка),
# время (дата + часы) + (без заголовка), название + время (дата))

# сделать чтобы эти записи отображались на ежедневнике
