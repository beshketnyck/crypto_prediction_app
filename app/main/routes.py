from flask import Blueprint, render_template, request, current_app
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.data_analyser import DataAnalyser
import datetime
import asyncio

main = Blueprint('main', __name__)

class DataForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    coin = SelectField('Cryptocurrency', choices=[('bitcoin', 'Bitcoin'), ('ethereum', 'Ethereum')])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    data = None
    twitter_followers = None
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        coin_id = form.coin.data

        # Перетворення start_date та end_date на datetime
        start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(end_date, datetime.datetime.min.time())

        # Тестування з меншою кількістю днів
        end_date = start_date + datetime.timedelta(days=10)

        analyser = DataAnalyser(current_app.config['BASE_API_URL'])

        async def fetch_data():
            data = await analyser.get_data(start_date, end_date, coin_id)
            twitter_followers = await analyser.fetch_twitter_followers(coin_id)
            if data is not None:
                filename = f'data/{coin_id}_{start_date.date()}_{end_date.date()}.csv'
                analyser.save_to_csv(data, filename)
            return data, twitter_followers

        data, twitter_followers = asyncio.run(fetch_data())

    return render_template('index.html', form=form, data=data, twitter_followers=twitter_followers)
