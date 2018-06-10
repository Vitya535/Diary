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
    today_Month, Month = datetime.now().month, datetime.now().month
    today_Year, Year = datetime.now().year, datetime.now().year

    @staticmethod
    def inst():
        if Calendar._instance is None:
            Calendar._instance = Calendar()
        return Calendar._instance

    @staticmethod
    @app.route('/up_month/', methods=['POST'])
    def up_month():
        if Calendar._instance.Month == 12:
            Calendar._instance.Month = 1
            Calendar._instance.Year += 1
        else:
            Calendar._instance.Month += 1
        return render_template('Calendar.html', calendar=Calendar.inst(), IsWeek=False)

    @staticmethod
    @app.route('/down_month/', methods=['POST'])
    def down_month():
        if Calendar._instance.Month == 1:
            Calendar._instance.Month = 12
            Calendar._instance.Year -= 1
        else:
            Calendar._instance.Month -= 1
        return render_template('Calendar.html', calendar=Calendar.inst(), IsWeek=False)

    @staticmethod
    @app.route('/up_week/', methods=['POST'])
    def up_week():
        if Calendar._instance.Month == 12:
            Calendar._instance.Month = 1
            Calendar._instance.Year += 1
        else:
            Calendar._instance.Month += 1
        return render_template('Calendar.html', calendar=Calendar.inst(), IsWeek=False)

    @staticmethod
    @app.route('/down_week/', methods=['POST'])
    def down_week():
        if Calendar._instance.Month == 1:
            Calendar._instance.Month = 12
            Calendar._instance.Year -= 1
        else:
            Calendar._instance.Month -= 1
        return render_template('Calendar.html', calendar=Calendar.inst(), IsToday=False)

    @staticmethod
    @app.route('/', methods=['POST'])
    def show_today():
        return render_template('Calendar.html', calendar=Calendar.inst(), IsToday=True)

# все хорошо конечно, но мне не нравится, что при листании календаря вся страница перезагружается


@app.route('/', methods=['GET', 'POST'])
def show_diary():
    return render_template('Calendar.html', calendar=Calendar.inst(), IsToday=False)


if __name__ == '__main__':
    Calendar.inst()
    print(datetime.now())
    app.run()
