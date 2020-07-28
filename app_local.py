from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, DATE
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from report import process_data, get_data
import os
import pandas as pd
import requests
import csv
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kinmengtan:kinmengtan@localhost:5432/stocks'
app.debug = True
db = SQLAlchemy(app)

from models import Result

def data_proc():
	stock_symbols_df = pd.read_csv('./stock_symbols/common_stocks_second_edition.csv')
	stock_symbols = stock_symbols_df['Symbol']
	stock_symbols = list(stock_symbols)
	#https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
	stock_symbols = [str(x).replace('\xa0', '') for x in stock_symbols]
	stock_name = stock_symbols_df['Name']
	stock_data = get_data(stock_symbols)
	print("reached_here")
	high_priority, low_priority, no_importance, unprocessed = process_data(stock_data,stock_symbols)
	print(high_priority)
	for sym, name in zip(stock_symbols, stock_name):
		print("entered loop")
		for key, value in high_priority.items():
			print(key,value)
			if key == sym:
				print(key, name, value)
				stock_data = Result(result=value, stock_name=name, stock_ticker=key)
				db.session.add(stock_data)
				db.session.commit()
	return "completed"


sched = BackgroundScheduler(daemon=True)
sched.add_job(data_proc,'interval', hours=6, timezone='UTC', jitter=1200)
sched.start()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/test/')
def test_save():
	stock_data = Result(result=[(('2020-07-20', 'oversold'), '2020-07-23')], stock_name="Abercrombie & Fitch Co.", stock_ticker="ANF")
	db.session.add(stock_data)
	db.session.commit()
	return "save completed"

@app.route('/results')
def get_result():
	final_results = {}

	results_today = db.session.query(Result).filter(cast(Result.date_generated, DATE) == date.today()-timedelta(days=1)).all()
	print(results_today)
	if results_today:
		if type(results_today) == list:
			for result in results_today:
				print(result.stock_ticker)
				if result.stock_ticker not in final_results:
					final_results[result.stock_ticker] = [result.stock_name, result.result, result.date_generated]
		else:
			final_results[results_today.stock_ticker] = [result.stock_name, result.result, result.date_generated]
	else:
		return "No results found"
	
 
	return render_template('index.html',result=final_results)


   

if __name__ == '__main__':
	app.run()
