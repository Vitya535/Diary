"""Данный модуль отвечает за базу данных и работу с ней"""
from sqlite3 import connect

CONN = connect("data_for_diary.db")  # создание связи с базой данных

CURSOR = CONN.cursor()
CURSOR.execute('''CREATE TABLE if not exists diary_events
                (event_title text, event_time text)''')
# создание таблицы: event_title - название события, event_time - время события
CONN.close()


def init_event_data():
    """инициализация списка представляющего
            собой данные из базы"""
    con = connect("data_for_diary.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM diary_events")
    con.commit()
    return cursor.fetchall()
    # здесь нет con.close(), интересно а насколько это опасно?


def add_data(add_title, add_time):
    """Добавление записи в базу данных"""
    con = connect("data_for_diary.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO diary_events VALUES(?, ?)",
                   (add_title, add_time))
    con.commit()
    con.close()


def del_data(del_title, del_time):
    """Удаление записи из базы данных"""
    con = connect("data_for_diary.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM diary_events WHERE event_title==? AND event_time==?",
                   (del_title, del_time))
    con.commit()
    con.close()


def update_data(new_time, new_title, old_title, old_time):
    """Редактирование записи в базе данных"""
    con = connect("data_for_diary.db")
    cursor = con.cursor()
    cursor.execute("UPDATE diary_events SET event_time=?, event_title=?"
                   " WHERE event_title==? AND event_time==?",
                   (new_time, new_title, old_title, old_time))
    con.commit()
    con.close()
