#!python3
#A simple Flask app that allows you to enter the last thing you ate and then display it on a
#second page.

from flask import Flask, render_template, request
import sqlite3

with sqlite3.connect("meal.db") as connection:
	c = connection.cursor()
	try:
		c.execute("""CREATE TABLE meals
				(names TEXT, foods TEXT, drinks TEXT)
				""")		
	except:
		pass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	info = []
	if request.method == 'POST' and 'name' in request.form:
		name = request.form.get('name')
		food = request.form.get('food')
		drink = request.form.get('drink')
		for i in (name, food, drink):
			info.append(i)
		with sqlite3.connect("meal.db") as connection:
			c = connection.cursor()
			c.execute("INSERT INTO meals VALUES(?, ?, ?)", info)
	return render_template('last_meal.html',
							info=info)
							
@app.route('/meal_history')
def meal_history():
	with sqlite3.connect("meal.db") as connection:
			c = connection.cursor()
	return render_template('meal_history.html',
							c=c)

app.run()
