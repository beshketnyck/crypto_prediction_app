from flask import Blueprint, render_template, request, current_app, send_file
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.data_analyser import DataAnalyser
import datetime
import os

main = Blueprint('main', __name__)

class DataForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    coin = SelectField('Cryptocurrency', choices=[('bitcoin', 'Bitcoin'), ('ethereum', 'Ethereum'), ('tether', 'Tether')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    data = None
    error = None
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        coin_id = form.coin.data

        # Отримання даних за вказаний період
        analyser = DataAnalyser(current_app.config['BASE_API_URL'])
        try:
            data = analyser.fetch_data(start_date, end_date, coin_id)

            # Збереження даних у CSV-файл
            filename = f'data_{coin_id}_{start_date}_{end_date}.csv'
            filepath = analyser.save_to_csv(data, filename)

            # Відображення точного шляху до файлу для налагодження
            print(f"Saving file to: {filepath}")

            return send_file(filepath, as_attachment=True)
        except ValueError as e:
            error = str(e)
        except FileNotFoundError as e:
            error = f"File not found: {str(e)}"
    return render_template('index.html', form=form, data=data, error=error)
