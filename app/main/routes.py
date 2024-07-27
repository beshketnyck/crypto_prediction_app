from flask import Blueprint, render_template, request, current_app
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.data_analyser import DataAnalyser
import datetime

main = Blueprint('main', __name__)

class DataForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    coin = SelectField('Cryptocurrency', choices=[('bitcoin', 'Bitcoin'), ('ethereum', 'Ethereum')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    data = None
    error = None

    if request.method == 'POST' and form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        coin_id = form.coin.data
        analyser = DataAnalyser(current_app.config['BASE_API_URL'])
        try:
            # Отримання даних за заданим діапазоном дат
            data = analyser.fetch_data(start_date, end_date, coin_id)
            filename = f'data_{coin_id}_{start_date}_{end_date}.csv'
            # Збереження даних у CSV файл
            filepath = analyser.save_to_csv(data, filename)
            # Зчитування даних з CSV для відображення
            data = analyser.read_csv(filepath)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = str(e)

    return render_template('index.html', form=form, data=data, error=error)
