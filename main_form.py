from flask import Flask, render_template
from calendar import HTMLCalendar, month_name, day_name, monthrange, weekday
from datetime import datetime, date
from locale import setlocale, LC_ALL

# сделать базу данных в SQLite
# время (дата.время тип данных)
# описание события (текст)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'NotTellAnyone'
setlocale(LC_ALL, '')


class Calendar(HTMLCalendar):
    _instance = None
    buf_for_select, down_title, up_title, url_up, url_down = \
        'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
    today_Day_format, Day_format = datetime.now().strftime('%a'), datetime.now().strftime('%a')
    today_Day, Day = datetime.now().day, datetime.now().day
    today_Month, Month, week_Month = datetime.now().month, datetime.now().month, datetime.now().month
    today_Year, Year, week_Year = datetime.now().year, datetime.now().year, datetime.now().year
    tuple_for_months_gen_case = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                                 'октября', 'ноября', 'декабря')
    first_type_day_in_month, last_type_day_in_month, weeks_in_month = 0, 0, 0
    this_week = today_Day // 5

    @staticmethod
    def get_first_type_day_in_month():
        buf = Calendar.inst().monthdays2calendar(Calendar.Year, Calendar.Month)
        for i in range(len(buf)):
            if buf[i][weekday(Calendar.Year, Calendar.Month, Calendar.Day)][0]:
                Calendar.first_type_day_in_month = buf[i][weekday(Calendar.Year, Calendar.Month, Calendar.Day)][0]
                break

    @staticmethod
    def get_last_type_day_in_month():
        buf = Calendar.inst().monthdays2calendar(Calendar.Year, Calendar.Month)
        for i in range(0, -len(buf), -1):
            if buf[i][weekday(Calendar.Year, Calendar.Month, Calendar.Day)][0]:
                Calendar.last_type_day_in_month = buf[i][weekday(Calendar.Year, Calendar.Month, Calendar.Day)][0]
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
        return day_name[datetime.now().isocalendar()[2]] + ', ' + str(Calendar.today_Day)\
               + ' ' + Calendar.tuple_for_months_gen_case[Calendar.today_Month - 1]

    @staticmethod
    def text_for_today_month_and_year():
        return month_name[Calendar.today_Month] + ' ' + str(Calendar.today_Year)

    @staticmethod
    @app.route('/up_month/', methods=['POST'])
    def up_month():
        print('up_month')
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
        else:
            Calendar.Month += 1
        # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='Месяц',
                               down_title='Предыдущий месяц', up_title='Следующий месяц', url_up='/up_month/',
                               url_down='/down_month/')

    @staticmethod
    @app.route('/down_month/', methods=['POST'])
    def down_month():
        print('down_month')
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Месяц', 'Предыдущий месяц', 'Следующий месяц', '/up_month/', '/down_month/'
        if Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
        else:
            Calendar.Month -= 1
        # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='Месяц',
                               down_title='Предыдущий месяц', up_title='Следующий месяц', url_up='/up_month/',
                               url_down='/down_month/')

    @staticmethod
    @app.route('/up_month_in_calendar/', methods=['POST'])
    def up_month_in_calendar():
        print('up_month_in_calendar')
        # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        if Calendar.Month == 12:
            Calendar.Month = 1
            Calendar.Year += 1
        else:
            Calendar.Month += 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select=Calendar.buf_for_select,
                               down_title=Calendar.down_title, up_title=Calendar.up_title, url_up=Calendar.url_up,
                               url_down=Calendar.url_down)

    @staticmethod
    @app.route('/down_month_in_calendar/', methods=['POST'])
    def down_month_in_calendar():
        print('down_month_in_calendar')
        # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        if Calendar.Month == 1:
            Calendar.Month = 12
            Calendar.Year -= 1
        else:
            Calendar.Month -= 1
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select=Calendar.buf_for_select,
                               down_title=Calendar.down_title, up_title=Calendar.up_title, url_up=Calendar.url_up,
                               url_down=Calendar.url_down)

    @staticmethod
    @app.route('/up_week_vertical/', methods=['POST'])
    def up_week_vertical():
        print('up_week_vertical')
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя', '/up_week_vertical/', '/down_week_vertical/'
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
            Calendar.get_last_type_day_in_month()
            Calendar.this_week = 1
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
            # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='Неделя',
                               down_title='Предыдущая неделя', up_title='Следующая неделя', url_up='/up_week_vertical/',
                               url_down='/down_week_vertical/')

    @staticmethod
    @app.route('/down_week_vertical/', methods=['POST'])
    def down_week_vertical():
        print('down_week_vertical')
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'Неделя', 'Предыдущая неделя', 'Следующая неделя', '/up_week_vertical/', '/down_week_vertical/'
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
            Calendar.get_first_type_day_in_month()
            Calendar.this_week = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
            Calendar.weeks_in_month = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
            Calendar.week_Month = Calendar.Month
            Calendar.week_Year = Calendar.Year
            # Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='Неделя',
                               down_title='Предыдущая неделя', up_title='Следующая неделя', url_up='/up_week_vertical/',
                               url_down='/down_week_vertical/')

    @staticmethod
    @app.route('/up_day/', methods=['POST'])
    def up_day():
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
        print('up_day')
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if Calendar.Day == Calendar.Day + 6 - weekday(Calendar.Year, Calendar.Month, Calendar.Day):
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
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='День',
                               down_title='Предыдущий день', up_title='Следующий день', url_up='/up_day/',
                               url_down='/down_day/')

    @staticmethod
    @app.route('/down_day/', methods=['POST'])
    def down_day():
        Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
            'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
        print('down_day')
        Calendar.Month = Calendar.week_Month
        Calendar.Year = Calendar.week_Year
        if Calendar.Day == Calendar.Day - weekday(Calendar.Year, Calendar.Month, Calendar.Day):
           Calendar.this_week -= 1
           Calendar.Day -= 1
        elif Calendar.Day == 1:
           Calendar.Month -= 1
           Calendar.Day = monthrange(Calendar.Year, Calendar.Month)[1]
           Calendar.this_week = (Calendar.last_type_day_in_month - Calendar.first_type_day_in_month) // 5
        elif Calendar.Month == 1:
           Calendar.Month = 12
           Calendar.Year -= 1
           Calendar.Day = monthrange(Calendar.Year, Calendar.Month)[1]
        else:
            Calendar.Day -= 1
        Calendar.week_Month = Calendar.Month
        Calendar.week_Year = Calendar.Year
        Calendar.Day_format = date(Calendar.Year, Calendar.Month, Calendar.Day).strftime('%a')
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='День',
                               down_title='Предыдущий день', up_title='Следующий день', url_up='/up_day/',
                               url_down='/down_day/')

    @staticmethod
    @app.route('/', methods=['POST'])
    def show_today():
        Calendar.Month, Calendar.week_Month = Calendar.today_Month, Calendar.today_Month
        Calendar.Year, Calendar.week_Year = Calendar.today_Year, Calendar.today_Year
        Calendar.Day = Calendar.today_Day
        Calendar.Day_format = Calendar.today_Day_format
        Calendar.this_week = Calendar.today_Day // 5
        return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), IsToday=True,
                               buf_for_select=Calendar.buf_for_select, down_title=Calendar.down_title,
                               up_title=Calendar.up_title, url_up=Calendar.url_up, url_down=Calendar.url_down)


@app.route('/', methods=['GET', 'POST'])
def show_diary():
    Calendar.buf_for_select, Calendar.down_title, Calendar.up_title, Calendar.url_up, Calendar.url_down = \
        'День', 'Предыдущий день', 'Следующий день', '/up_day/', '/down_day/'
    return render_template('ExtendPageWithDiary', calendar=Calendar.inst(), buf_for_select='День',
                           down_title='Предыдущий день', up_title='Следующий день', url_up='/up_day/',
                           url_down='/down_day/')


if __name__ == '__main__':
    Calendar.inst()
    print()
    app.run()
    # неделю лучше отрендерить в цикле
    # для рендеринга недели:
    # последний день недели = цифра любого дня в этой неделе + 6 - номер этого дня в неделе
    # первый день недели = цифра любого дня в этой неделе - номер этого дня в неделе
