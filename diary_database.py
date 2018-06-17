import sqlite3

conn = sqlite3.connect("data_for_diary.db")  # создание связи с базой данных
cursor = conn.cursor()  # обьект, позволящий взаимодействовать с базой данных, добавлять записи и т. д.

cursor.execute('''CREATE TABLE diary_events
                (event_title text, event_time text)''')
# создание таблицы: event_title - название события, event_time - время события


def get_connect():
    return conn


def update_record(new_title, new_time, old_title, old_time):
    t = new_time, new_title, old_title, old_time
    cursor.execute("UPDATE diary_events SET event_time=?, event_title=? WHERE event_title==? AND event_time==?", t)
    conn.commit()


def delete_record(title, time):
    t = title, time
    cursor.execute("DELETE FROM diary_events WHERE event_title==? AND event_time==?", t)
    conn.commit()


def add_record(add_title, add_time):
    t = add_title, add_time
    cursor.execute("INSERT INTO diary_events VALUES(?)", t)
    conn.commit()
# сделать чтобы эти записи отображались на ежедневнике
