from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
import datetime

main = Blueprint('main', __name__)

class DateForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DateForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        # Тут можна додати логіку для обробки даних
        return render_template('index.html', form=form, start_date=start_date, end_date=end_date)
    return render_template('index.html', form=form)
