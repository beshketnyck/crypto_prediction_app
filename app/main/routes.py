from flask import Blueprint, render_template, request, current_app
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from app.data_analyser import DataAnalyser

main = Blueprint('main', __name__)

class DateForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DateForm()
    data = None
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Отримання даних за вказаний період
        analyser = DataAnalyser(current_app.config['API_URL'])
        data = analyser.fetch_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        return render_template('index.html', form=form, start_date=start_date, end_date=end_date, data=data)
    return render_template('index.html', form=form, data=data)
