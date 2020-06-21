"""Данный модуль отвечает за базу данных и работу с ней"""
from sqlite3 import connect

SELECT_ALL_FROM_DIARY_EVENTS = "SELECT * FROM diary_events"
INSERT_INTO_DIARY_EVENTS = "INSERT INTO diary_events VALUES(?, ?)"
DELETE_FROM_DIARY_EVENTS = "DELETE FROM diary_events WHERE event_title==? AND event_time==?"
UPDATE_DIARY_EVENTS = "UPDATE diary_events SET event_time=?, event_title=? WHERE event_title==? AND event_time==?"


def execute_sql(func, *args, **kwargs):
    """Декоратор для соединения с БД"""

    def wrapper():
        """Функция-обертка"""
        with connect("data_for_diary.db") as con:
            cur = con.cursor()
            return func(cur, *args, **kwargs)

    return wrapper


@execute_sql
def init_event_data(cur) -> list:
    """Инициализация списка представляющего собой данные из базы"""
    cur.execute(SELECT_ALL_FROM_DIARY_EVENTS)
    return cur.fetchall()


@execute_sql
def add_data(cur, add_title: str, add_time: str) -> None:
    """Добавление записи в базу данных"""
    cur.execute(INSERT_INTO_DIARY_EVENTS, (add_title, add_time))


@execute_sql
def del_data(cur, del_title: str, del_time: str) -> None:
    """Удаление записи из базы данных"""
    cur.execute(DELETE_FROM_DIARY_EVENTS, (del_title, del_time))


@execute_sql
def update_data(cur, new_time: str, new_title: str, old_title: str, old_time: str) -> None:
    """Редактирование записи в базе данных"""
    cur.execute(UPDATE_DIARY_EVENTS, (new_time, new_title, old_title, old_time))
