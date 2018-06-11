from flask import Flask, render_template
from calendar import HTMLCalendar
from datetime import datetime

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'NotTellAnyone'


class Calendar(HTMLCalendar):
    _instance = None
    today_Day, Day = datetime.now().day, datetime.now().day
    today_Month, Month, week_Month = datetime.now().month, datetime.now().month, datetime.now().month
    today_Year, Year, week_Year = datetime.now().year, datetime.now().year, datetime.now().year
    tuple_for_days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
    tuple_for_months_gen_case = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                                 'октября', 'ноября', 'декабря')
    tuple_for_months_nom_case = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                                 'Октябрь', 'Ноябрь', 'Декабрь')
    first_type_day_in_month, last_type_day_in_month, weeks_in_month = 0, 0, 0
    this_week = today_Day // 5

    @staticmethod
    def get_first_type_day_in_month():
        buf = Calendar._instance.monthdatescalendar(Calendar.Year, Calendar.Month)
        for i in range(len(buf)):
            if buf[i][datetime.now().isocalendar()[2] - 1].month == Calendar.Month:
                Calendar.first_type_day_in_month = buf[i][datetime.now().isocalendar()[2] - 1].day
                break

    @staticmethod
    def get_last_type_day_in_month():
        buf = Calendar._instance.monthdatescalendar(Calendar.Year, Calendar.Month)
        for i in range(0, -len(buf), -1):
            if buf[i][datetime.now().isocalendar()[2] - 1].month == Calendar.Month:
                Calendar.last_type_day_in_month = buf[i][datetime.now().isocalendar()[2] - 1].day
                break

    @staticmethod
    def inst():
        if Calendar._instance is None:
            Calendar._instance = Calendar()
            Calendar.get_first_type_day_in_month()
            Calendar.get_last_type_day_in_month()
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
        return Calendar._instance

    @staticmethod
    def title_for_today():
        return str(Calendar.tuple_for_days[datetime.now().isocalendar()[2] - 1]) + ', ' + str(Calendar.today_Day)\
               + ' ' + Calendar.tuple_for_months_gen_case[Calendar.today_Month - 1]

    @staticmethod
    def text_for_today_month_and_year():
        return Calendar.tuple_for_months_nom_case[Calendar.today_Month - 1] + ' ' + str(Calendar.today_Year)

    @staticmethod
    @app.route('/up_month/', methods=['POST'])
    def up_month():
        if Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
        else:
            Calendar.Month += 1
        return render_template('Calendar.html', calendar=Calendar.inst())

    @staticmethod
    @app.route('/down_month/', methods=['POST'])
    def down_month():
        if Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
        else:
            Calendar.Month -= 1
        return render_template('Calendar.html', calendar=Calendar.inst())

    @staticmethod
    @app.route('/up_week/', methods=['POST'])
    def up_week():
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if Calendar.this_week != Calendar.weeks_in_month:
            Calendar.this_week += 1
            Calendar.Day += 7
        else:
            Calendar.up_month()
            Calendar.get_first_type_day_in_month()
            Calendar.get_last_type_day_in_month()
            Calendar.this_week = 1
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
            Calendar.Day = Calendar.first_type_day_in_month
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
        return render_template('Calendar.html', calendar=Calendar.inst())

    @staticmethod
    @app.route('/down_week/', methods=['POST'])
    def down_week():
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if Calendar.this_week != 1:
            Calendar.this_week -= 1
            Calendar.Day -= 7
        else:
            Calendar.down_month()
            Calendar.get_first_type_day_in_month()
            Calendar.get_last_type_day_in_month()
            Calendar.this_week = Calendar.last_type_day_in_month // 5 - 1
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
            Calendar.Day = Calendar.last_type_day_in_month
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
        return render_template('Calendar.html', calendar=Calendar.inst())

    @staticmethod
    @app.route('/', methods=['POST'])
    def show_today():
        Calendar.Month, Calendar.week_Month = Calendar.today_Month, Calendar.today_Month
        Calendar.Year, Calendar.week_Year = Calendar.today_Year, Calendar.today_Year
        Calendar.Day = Calendar.today_Day
        return render_template('Calendar.html', calendar=Calendar.inst(), IsToday=True)


@app.route('/', methods=['GET', 'POST'])
def show_diary():
    return render_template('Calendar.html', calendar=Calendar.inst())


if __name__ == '__main__':
    Calendar.inst()
    app.run()
