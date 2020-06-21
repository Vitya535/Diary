"""Данный модуль отвечает за серверную часть приложения"""
from calendar import HTMLCalendar
from calendar import monthrange
from calendar import weekday
from datetime import date
from datetime import datetime
from re import findall

from flask import render_template
from flask import request
from htmlmin import minify

from app import APP
from app import utils
from app.diary_database import add_data
from app.diary_database import del_data
from app.diary_database import init_event_data
from app.diary_database import update_data


@APP.template_filter('regexp_split')
def regexp_split(string: str) -> list:
    """Фильтр для разбиения строки по регулярному выражению"""
    split = findall(r"[\w]+", string)
    return split


@APP.context_processor
def inject_common_template_params() -> dict:
    return dict(calendar=Calendar.inst(),
                cls=Calendar,
                utils=utils)


class Calendar(HTMLCalendar):
    """Класс календаря"""
    _instance = None
    event_data = init_event_data()
    buf_for_select, down_title, up_title, url_up, url_down = \
        'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
    today_day_format = day_format = datetime.now().strftime('%a')
    today_day = day = datetime.now().day
    today_month = month = week_month = datetime.now().month
    today_year = year = week_year = datetime.now().year
    first_type_day_in_month = last_type_day_in_month = weeks_in_month = 0
    this_week = today_day // 5

    # взаимодействие с базой данных
    @staticmethod
    @APP.route('/update_data/', methods=['POST'])
    def update_record():
        """Редактирование записи в базе данных"""
        new_title = request.form['description_of_event']
        new_time = request.form['time_of_event']
        split_time = new_time.split('-')
        new_time = f"{Calendar.year}-{Calendar.month}-{Calendar.day} 0{split_time[0]}:00.000"
        addition = request.form['additional']
        split_addition = addition.split('<br>')
        old_title = split_addition[0]
        time = split_addition[1].split('-')
        old_time = f"{Calendar.year}-{Calendar.month}-{Calendar.day} 0{time[0]}:00.000"
        update_data(new_time, new_title, old_title, old_time)
        index_of_data = Calendar.event_data.index((old_title, old_time))
        Calendar.event_data[index_of_data] = (new_title, new_time)
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/del_data/', methods=['POST'])
    def delete_record():
        """Удаление записи из базы данных"""
        del_title = request.form['description_of_event']
        del_time = request.form['time_of_event']
        split_del_time = del_time.split('-')
        del_time = f"{Calendar.year}-{Calendar.month}-{Calendar.day} 0{split_del_time[0]}:00.000"
        del_data(del_title, del_time)
        Calendar.event_data.remove((del_title, del_time))
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/add_data/', methods=['POST'])
    def add_record():
        """Добавление записи в базу данных"""
        add_title = request.form['description_of_event']
        add_time = request.form['time_of_event']
        split_add_time = findall(r"[\w'^:]+", add_time)
        add_time = f"{split_add_time[2]}-{str(utils.TUPLE_FOR_MONTHS_GEN_CASE.index(split_add_time[1]) + 1)}-" \
                   f"{split_add_time[0]} 0{split_add_time[3]}:00.000"
        add_data(add_title, add_time)
        Calendar.event_data.append((add_title, add_time))
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    def inst():
        """Инициализация календаря через одиночку"""
        if Calendar._instance is None:
            Calendar._instance = Calendar()
            Calendar.first_type_day_in_month = utils.get_first_type_day_in_month(
                Calendar.inst(), Calendar.year, Calendar.month, Calendar.day)
            Calendar.last_type_day_in_month = utils.get_last_type_day_in_month(
                Calendar.inst(), Calendar.year, Calendar.month, Calendar.day)
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
        return Calendar._instance

    @staticmethod
    @APP.route('/up_month/', methods=['POST'])
    def up_month():
        """Пролистывание ежедневника по месяцам вперед"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.month == 12:
            Calendar.month = 1
            Calendar.year += 1
        else:
            Calendar.month += 1
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/down_month/', methods=['POST'])
    def down_month():
        """Пролистывание ежедневника по месяцам назад"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.month == 1:
            Calendar.month = 12
            Calendar.year -= 1
        else:
            Calendar.month -= 1
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/up_month_in_calendar/', methods=['POST'])
    def up_month_in_calendar():
        """Пролистывание календаря по месяцам вперед"""
        if Calendar.month == 12:
            Calendar.month = 1
            Calendar.year += 1
        else:
            Calendar.month += 1
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/down_month_in_calendar/', methods=['POST'])
    def down_month_in_calendar():
        """Пролистывание календаря по месяцам назад"""
        if Calendar.month == 1:
            Calendar.month = 12
            Calendar.year -= 1
        else:
            Calendar.month -= 1
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/up_week_vertical/', methods=['POST'])
    def up_week_vertical():
        """Пролистывание календаря по неделям вперед вертикально"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя', '/up_week_vertical/', '/down_week_vertical/'
        if Calendar.this_week != Calendar.weeks_in_month:
            Calendar.this_week += 1
            Calendar.day += 7
        else:
            if monthrange(Calendar.year, Calendar.month)[1] == 30:
                Calendar.day -= 23
            else:
                Calendar.day -= 24
            Calendar.up_month()
            Calendar.first_type_day_in_month = Calendar.day
            Calendar.last_type_day_in_month = utils.get_last_type_day_in_month(
                Calendar.inst(), Calendar.year, Calendar.month, Calendar.day)
            Calendar.this_week = 1
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
            Calendar.week_month = Calendar.month
            Calendar.week_year = Calendar.year
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/down_week_vertical/', methods=['POST'])
    def down_week_vertical():
        """Пролистывание календаря по месяцам назад вертикально"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя', '/up_week_vertical/', '/down_week_vertical/'
        if Calendar.this_week != 1:
            Calendar.this_week -= 1
            Calendar.day -= 7
        else:
            if monthrange(Calendar.year, Calendar.month)[1] == 30:
                Calendar.day += 24
            else:
                Calendar.day += 23
            Calendar.down_month()
            Calendar.last_type_day_in_month = Calendar.day
            Calendar.first_type_day_in_month = utils.get_first_type_day_in_month(
                Calendar.inst(), Calendar.year, Calendar.month, Calendar.day)
            Calendar.this_week = (Calendar.last_type_day_in_month -
                                  Calendar.first_type_day_in_month) // 5
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
            Calendar.week_month = Calendar.month
            Calendar.week_year = Calendar.year
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/up_day/', methods=['POST'])
    def up_day():
        """Пролистывание календаря по дням вперед"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
        Calendar.month = Calendar.week_month
        Calendar.year = Calendar.week_year
        if weekday(Calendar.year, Calendar.month, Calendar.day) == 6:
            Calendar.this_week += 1
            Calendar.day += 1
        elif Calendar.day == monthrange(Calendar.year, Calendar.month)[1]:
            Calendar.month += 1
            Calendar.day = 1
            Calendar.this_week = 1
        elif Calendar.month == 12:
            Calendar.month = 1
            Calendar.year += 1
            Calendar.day = 1
        else:
            Calendar.day += 1
        Calendar.week_month = Calendar.month
        Calendar.week_year = Calendar.year
        Calendar.day_format = date(Calendar.year, Calendar.month, Calendar.day).strftime('%a')
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/down_day/', methods=['POST'])
    def down_day():
        """Пролистывание календаря по дням назад"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
        Calendar.month = Calendar.week_month
        Calendar.year = Calendar.week_year
        if not weekday(Calendar.year, Calendar.month, Calendar.day):
            Calendar.this_week -= 1
            Calendar.day -= 1
        elif Calendar.day == 1:
            Calendar.month -= 1
            Calendar.day = monthrange(Calendar.year, Calendar.month)[1]
            Calendar.this_week = (Calendar.last_type_day_in_month -
                                  Calendar.first_type_day_in_month) // 5
        elif Calendar.month == 1:
            Calendar.month = 12
            Calendar.year -= 1
            Calendar.day = monthrange(Calendar.year, Calendar.month)[1]
        else:
            Calendar.day -= 1
        Calendar.week_month = Calendar.month
        Calendar.week_year = Calendar.year
        Calendar.day_format = date(Calendar.year, Calendar.month, Calendar.day).strftime('%a')
        return minify(render_template('public/ExtendPageWithDiary.html'))

    @staticmethod
    @APP.route('/today/', methods=['POST'])
    def show_today():
        """Вернуться в календаре на месяц сегодняшнего дня"""
        Calendar.month = Calendar.week_month = Calendar.today_month
        Calendar.year = Calendar.week_year = Calendar.today_year
        Calendar.day = Calendar.today_day
        Calendar.day_format = Calendar.today_day_format
        Calendar.this_week = Calendar.today_day // 5
        return minify(render_template('public/ExtendPageWithDiary.html', IsToday=True))


@APP.route('/', methods=['GET', 'POST'])
def show_diary():
    """Изначальный показ веб-страницы"""
    return minify(render_template('public/ExtendPageWithDiary.html', IsToday=True))
