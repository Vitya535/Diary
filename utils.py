from calendar import weekday, day_name, month_name

tuple_for_months_gen_case = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                             'октября', 'ноября', 'декабря')


def get_first_type_day_in_month(instance, year, month, day):
    """Получение первого дня определенного типа в месяце"""
    buf = instance.monthdays2calendar(year, month)
    for i in range(len(buf)):
        if buf[i][weekday(year, month, day)][0]:
            return buf[i][weekday(year, month, day)][0]


def get_last_type_day_in_month(instance, year, month, day):
    """Получение последнего дня определенного типа в месяце"""
    buf = instance.monthdays2calendar(year, month)
    for i in range(0, -len(buf), -1):
        if buf[i][weekday(year, month, day)][0]:
            return buf[i][weekday(year, month, day)][0]


def title_for_today(today_day, today_month, today_year):
    """Возвращает текст всплывающей подсказки для сегодняшнего дня"""
    return day_name[weekday(today_year, today_month, today_day)].capitalize() + ', ' + str(today_day)\
           + ' ' + tuple_for_months_gen_case[today_month - 1]


def for_input_time_today(day, month, year):
    """Возвращает текст для input времени в всплывающей форме"""
    return str(day) + ' ' + tuple_for_months_gen_case[month - 1] + ' ' + str(year)


def text_for_today_month_and_year(today_month, today_year):
    """Возвращает текст для названия месяца и года"""
    return month_name[today_month] + ' ' + str(today_year)
