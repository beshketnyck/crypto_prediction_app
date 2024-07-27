from flask import Blueprint, render_template, request, send_file, current_app
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.data_analyser import DataAnalyser
import datetime

main = Blueprint('main', __name__)

class DataForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    coin = SelectField('Cryptocurrency', choices=[('bitcoin', 'Bitcoin'), ('ethereum', 'Ethereum'), ('dogecoin', 'Dogecoin')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    data = None
    social_data = None
    news = None
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        coin_id = form.coin.data
        
        analyser = DataAnalyser(current_app.config['BASE_API_URL'])
        
        try:
            data = analyser.fetch_data(start_date, end_date, coin_id)
            social_data = analyser.fetch_social_data(coin_id)
            news = analyser.fetch_news(coin_id)
            
            filename = f'data_{coin_id}_{start_date}_{end_date}.csv'
            filepath = analyser.save_to_csv(data, filename)
        except ValueError as e:
            return render_template('index.html', form=form, error=f"Error: {str(e)}")
        
    return render_template('index.html', form=form, data=data, social_data=social_data, news=news)
