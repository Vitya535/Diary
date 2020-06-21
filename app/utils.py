"""Данный модуль отвечает за различные вспомогательные функции для календаря"""
from calendar import day_name
from calendar import month_name
from calendar import weekday

TUPLE_FOR_MONTHS_GEN_CASE = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                             'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')


def get_first_type_day_in_month(instance, year: int, month: int, day: int) -> int:
    """Получение первого дня определенного типа в месяце"""
    buf = instance.monthdays2calendar(year, month)
    return buf[0][weekday(year, month, day)][0]


def get_last_type_day_in_month(instance, year: int, month: int, day: int) -> int:
    """Получение последнего дня определенного типа в месяце"""
    buf = instance.monthdays2calendar(year, month)
    return buf[-1][weekday(year, month, day)][0]


def title_for_today(today_day: int, today_month: int, today_year: int) -> str:
    """Возвращает текст всплывающей подсказки для сегодняшнего дня"""
    return f"{day_name[weekday(today_year, today_month, today_day)].capitalize()}, " \
           f"{today_day} {TUPLE_FOR_MONTHS_GEN_CASE[today_month - 1]}"


def for_input_time_today(day: int, month: int, year: int) -> str:
    """Возвращает текст для input времени в всплывающей форме"""
    return f"{day} {TUPLE_FOR_MONTHS_GEN_CASE[month - 1]} {year}"


def text_for_today_month_and_year(today_month: int, today_year: int) -> str:
    """Возвращает текст для названия месяца и года"""
    return f"{month_name[today_month]} {today_year}"
