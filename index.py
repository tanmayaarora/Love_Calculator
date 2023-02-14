import os
import logging
from flask import Flask, request, render_template


app = Flask(__name__)


# various Flask explanations available at:  https://flask.palletsprojects.com/en/1.1.x/quickstart/

		
def doRender(tname='index.htm', values={}):
	values['user_image'] = "./static/wallpaper.jpg"
	return render_template(tname, **values)	 


@app.route('/hello')
# Keep a Hello World message to show that at least something is working
def hello():
	return 'Hello World!'

# Defines a POST supporting calculate route
@app.route('/calculate',methods=['POST'])
def riskcalculator():

	name1 = request.form.get('name1')
	name2 = request.form.get('name2')

	lowercase_name1 = name1.lower()
	lowercase_name2 = name2.lower()

	t_count = lowercase_name1.count("t") + lowercase_name2.count("t")
	r_count = lowercase_name1.count("r") + lowercase_name2.count("r")
	u_count = lowercase_name1.count("u") + lowercase_name2.count("u")
	e_count = lowercase_name1.count("e") + lowercase_name2.count("e")

	l_count = lowercase_name1.count("l") + lowercase_name2.count("l")
	o_count = lowercase_name1.count("o") + lowercase_name2.count("o")
	v_count = lowercase_name2.count("v") + lowercase_name2.count("v")

	love_score = (10 * (t_count + r_count + u_count + e_count)) + l_count + o_count + v_count + e_count

	result = ""
	
	if love_score < 10 or love_score > 90:
		result = f"Your love score is {love_score}, you go together like coke and mentos"
	elif love_score >=40 and love_score <=50:
		result = f"Your love score is {love_score}, you are alright together"
	else:
		result = f"Your love score is {love_score}"
	return doRender('index.htm',{'output':result})

# catch all other page requests - doRender checks if a page is available (shows it) or not (index)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def mainPage(path):
	return doRender('index.htm')

@app.errorhandler(500)
# A small bit of error handling
def server_error(e):
	logging.exception('ERROR!')
	return """
	An  error occurred: <pre>{}</pre>
	""".format(e), 500

if __name__ == '__main__':
	# Entry point for running on the local machine
	# On GAE, endpoints (e.g. /) would be called.
	# Called as: gunicorn -b :$PORT index:app,
	# host is localhost; port is 8080; this file is index (.py)

	app.run(host='127.0.0.1', port=8080, debug=True)
