"""Данный модуль отвечает за серверную часть приложения"""
from calendar import HTMLCalendar, monthrange, weekday
from re import findall
from datetime import datetime, date
from locale import setlocale, LC_ALL
from flask import Flask, render_template, request
import utils
import diary_database

# App config.
DEBUG = True
APP = Flask(__name__)
APP.config.from_object(__name__)
APP.config['SECRET_KEY'] = 'NotTellAnyone'
setlocale(LC_ALL, '')


@APP.template_filter('regexp_split')
def regexp_split(string):
    """Фильтр для разбиения строки по регулярному выражению"""
    split = findall(r"[\w]+", string)
    return split


class Calendar(HTMLCalendar):
    """Класс календаря"""
    _instance = None
    event_data = diary_database.init_event_data()
    buf_for_select, down_title, up_title, url_up, url_down = \
        'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
    TODAY_DAY_FORMAT, Day_format = datetime.now().strftime('%a'), datetime.now().strftime('%a')
    TODAY_DAY, Day = datetime.now().day, datetime.now().day
    TODAY_MONTH, Month = datetime.now().month, datetime.now().month
    week_Month = datetime.now().month
    TODAY_YEAR, Year, week_Year = datetime.now().year, datetime.now().year, datetime.now().year
    first_type_day_in_month, last_type_day_in_month, weeks_in_month = 0, 0, 0
    this_week = TODAY_DAY // 5

    # взаимодействие с базой данных
    @staticmethod
    @APP.route('/update_data/', methods=['POST'])
    def update_record():
        """Редактирование записи в базе данных"""
        new_title = request.form['description_of_event']
        new_time = request.form['time_of_event']
        split_time = new_time.split('-')
        new_time = str(Calendar.Year) + '-' + str(Calendar.Month) + '-' + \
            str(Calendar.Day) + ' 0' + str(split_time[0]) + ':00.000'
        addition = request.form['additional']
        split_addition = addition.split('<br>')
        old_title = split_addition[0]
        time = split_addition[1].split('-')
        old_time = str(Calendar.Year) + '-' + str(Calendar.Month) + '-' + \
            str(Calendar.Day) + ' 0' + str(time[0]) + ':00.000'
        diary_database.update_data(new_time, new_title, old_title, old_time)
        index_of_data = Calendar.event_data.index((old_title, old_time))
        Calendar.event_data[index_of_data] = (new_title, new_time)
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/del_data/', methods=['POST'])
    def delete_record():
        """Удаление записи из базы данных"""
        del_title = request.form['description_of_event']
        del_time = request.form['time_of_event']
        split_del_time = del_time.split('-')
        del_time = str(Calendar.Year) + '-' + str(Calendar.Month) + '-'\
            + str(Calendar.Day) + ' 0' + str(split_del_time[0]) + ':00.000'
        diary_database.del_data(del_title, del_time)
        Calendar.event_data.remove((del_title, del_time))
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/add_data/', methods=['POST'])
    def add_record():
        """Добавление записи в базу данных"""
        add_title = request.form['description_of_event']
        add_time = request.form['time_of_event']
        split_add_time = findall(r"[\w'^:]+", add_time)
        add_time = split_add_time[2] + '-' + \
            str(utils.TUPLE_FOR_MONTHS_GEN_CASE.index(split_add_time[1]) + 1)\
            + '-' + split_add_time[0] + ' 0' + split_add_time[3] + ':00.000'
        diary_database.add_data(add_title, add_time)
        Calendar.event_data.append((add_title, add_time))
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    def inst():
        """Инициализация календаря через одиночку"""
        if Calendar._instance is None:
            Calendar._instance = Calendar()
            Calendar.first_type_day_in_month = utils.get_first_type_day_in_month(
                Calendar.inst(), Calendar.Year, Calendar.Month, Calendar.Day)
            Calendar.last_type_day_in_month = utils.get_last_type_day_in_month(
                Calendar.inst(), Calendar.Year, Calendar.Month, Calendar.Day)
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
        return Calendar._instance

    @staticmethod
    @APP.route('/up_month/', methods=['POST'])
    def up_month():
        """Пролистывание ежедневника по месяцам вперед"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
        else:
            Calendar.Month += 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/down_month/', methods=['POST'])
    def down_month():
        """Пролистывание ежедневника по месяцам назад"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
        else:
            Calendar.Month -= 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/up_month_in_calendar/', methods=['POST'])
    def up_month_in_calendar():
        """Пролистывание календаря по месяцам вперед"""
        if Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
        else:
            Calendar.Month += 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/down_month_in_calendar/', methods=['POST'])
    def down_month_in_calendar():
        """Пролистывание календаря по месяцам назад"""
        if Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
        else:
            Calendar.Month -= 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/up_week_vertical/', methods=['POST'])
    def up_week_vertical():
        """Пролистывание календаря по неделям вперед вертикально"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя',\
            '/up_week_vertical/', '/down_week_vertical/'
        if Calendar.this_week != Calendar.weeks_in_month:
            Calendar.this_week += 1
            Calendar.Day += 7
        else:
            if monthrange(Calendar.Year, Calendar.Month)[1] == 30:
                Calendar.Day -= 23
            else:
                Calendar.Day -= 24
            Calendar.up_month()
            Calendar.first_type_day_in_month = Calendar.Day
            Calendar.last_type_day_in_month = utils.get_last_type_day_in_month(
                Calendar.inst(), Calendar.Year, Calendar.Month, Calendar.Day)
            Calendar.this_week = 1
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/down_week_vertical/', methods=['POST'])
    def down_week_vertical():
        """Пролистывание календаря по месяцам назад вертикально"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя',\
            '/up_week_vertical/', '/down_week_vertical/'
        if Calendar.this_week != 1:
            Calendar.this_week -= 1
            Calendar.Day -= 7
        else:
            if monthrange(Calendar.Year, Calendar.Month)[1] == 30:
                Calendar.Day += 24
            else:
                Calendar.Day += 23
            Calendar.down_month()
            Calendar.last_type_day_in_month = Calendar.Day
            Calendar.first_type_day_in_month = utils.get_first_type_day_in_month(
                Calendar.inst(), Calendar.Year, Calendar.Month, Calendar.Day)
            Calendar.this_week = (Calendar.last_type_day_in_month -
                                  Calendar.first_type_day_in_month) // 5
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month -
                                       Calendar.first_type_day_in_month) // 5
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/up_day/', methods=['POST'])
    def up_day():
        """Пролистывание календаря по дням вперед"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день',\
            '/up_day/', '/down_day/'
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if weekday(Calendar.Year, Calendar.Month, Calendar.Day) == 6:
            Calendar.this_week += 1
            Calendar.Day += 1
        elif Calendar.Day == monthrange(Calendar.Year, Calendar.Month)[1]:
            Calendar.Month += 1
            Calendar.Day = 1
            Calendar.this_week = 1
        elif Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
            Calendar.Day = 1
        else:
            Calendar.Day += 1
        Calendar.week_Month = Calendar.Month
        Calendar.week_Year = Calendar.Year
        Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/down_day/', methods=['POST'])
    def down_day():
        """Пролистывание календаря по дням назад"""
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title,\
            Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if not weekday(Calendar.Year, Calendar.Month, Calendar.Day):
            Calendar.this_week -= 1
            Calendar.Day -= 1
        elif Calendar.Day == 1:
            Calendar.Month -= 1
            Calendar.Day = monthrange(Calendar.Year, Calendar.Month)[1]
            Calendar.this_week = (Calendar.last_type_day_in_month -
                                  Calendar.first_type_day_in_month) // 5
        elif Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
            Calendar.Day = monthrange(Calendar.Year, Calendar.Month)[1]
        else:
            Calendar.Day -= 1
        Calendar.week_Month = Calendar.Month
        Calendar.week_Year = Calendar.Year
        Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(),
                               cls=Calendar, utils=utils)

    @staticmethod
    @APP.route('/today/', methods=['POST'])
    def show_today():
        """Вернуться в календаре на месяц сегодняшнего дня"""
        Calendar.Month, Calendar.week_Month = Calendar.TODAY_MONTH, Calendar.TODAY_MONTH
        Calendar.Year, Calendar.week_Year = Calendar.TODAY_YEAR, Calendar.TODAY_YEAR
        Calendar.Day = Calendar.TODAY_DAY
        Calendar.Day_format = Calendar.TODAY_DAY_FORMAT
        Calendar.this_week = Calendar.TODAY_DAY // 5
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), IsToday=True,
                               cls=Calendar, utils=utils)


@APP.route('/', methods=['GET', 'POST'])
def show_diary():
    """Изначальный показ веб-страницы"""
    return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), IsToday=True,
                           cls=Calendar, utils=utils)


if __name__ == '__main__':
    Calendar.inst()
    APP.run()
