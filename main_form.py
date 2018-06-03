from flask import Flask, render_template
from wtforms.widgets import SubmitInput
from calendar import HTMLCalendar
from datetime import datetime

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'NotTellAnyone'


class Calendar(HTMLCalendar):
    _instance = None
    today_Day = datetime.now().day
    today_Month = datetime.now().month
    today_Year = datetime.now().year
    turn_down = SubmitInput()
    turn_up = SubmitInput()

    @staticmethod
    def inst():
        if Calendar._instance is None:
            Calendar._instance = Calendar()
        return Calendar._instance

    @staticmethod
    @app.route('/up/', methods=['GET', 'POST'])
    def up():
        if Calendar._instance.today_Month == 12:
            Calendar._instance.today_Month = 1
            Calendar._instance.today_Year += 1
        else:
            Calendar._instance.today_Month += 1
        return render_template('Calendar.html', calendar=Calendar.inst(), Up=Calendar.turn_up, Down=Calendar.turn_down)

    @staticmethod
    @app.route('/down/', methods=['GET', 'POST'])
    def down():
        if Calendar._instance.today_Month == 1:
            Calendar._instance.today_Month = 12
            Calendar._instance.today_Year -= 1
        else:
            Calendar._instance.today_Month -= 1
        return render_template('Calendar.html', calendar=Calendar.inst(), Up=Calendar.turn_up, Down=Calendar.turn_down)

# <link rel="stylesheet" href="CalendarStyle.css" type="text/css"> - так почему-то не работает


@app.route('/', methods=['GET', 'POST'])  # CSS не работает, надо разобраться!
def hello_world():
    Calendar.inst()
    return render_template('Calendar.html', calendar=Calendar.inst(), Up=Calendar.turn_up, Down=Calendar.turn_down)


if __name__ == '__main__':
    app.run()
