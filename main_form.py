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


@app.route('/', methods=['GET', 'POST'])  # CSS не работает, надо разобраться!
def hello_world():
    Calendar.inst()
    with open('templates/Calendar.html', 'w') as g:
        g.write('<link rel="stylesheet" href="CalendarStyle.css" type="text/css"/>\n<title>Web-Diary</title>\n'
                + Calendar.inst().formatmonth(Calendar.today_Year, Calendar.today_Month))
    return render_template('Calendar.html')


if __name__ == '__main__':
    app.run()
