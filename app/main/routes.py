from flask import Blueprint, render_template, request, current_app
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.data_analyser import DataAnalyser
import datetime

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
        
        analyser = DataAnalyser(current_app.config['BASE_API_URL'])
        
        try:
            data = analyser.fetch_data(start_date, end_date, coin_id)
            twitter_followers = analyser.fetch_twitter_followers(coin_id)
            
            filename = f'data_{coin_id}_{start_date}_{end_date}.csv'
            filepath = analyser.save_to_csv(data, filename)
        except ValueError as e:
            return render_template('index.html', form=form, error=f"Error: {str(e)}")
        
    return render_template('index.html', form=form, data=data, twitter_followers=twitter_followers)
