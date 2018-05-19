from flask import Flask
from wtforms.widgets import TableWidget
from wtforms import Form, StringField
app = Flask(__name__)


class MyForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/hello')
def hello():
    return 'Hello'


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    F = MyForm()
    app.run(debug=True)
