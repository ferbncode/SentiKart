from flask import Flask, render_template

app = Flask(__name__)

@app.route('/qanda')
def mainpage():
	return render_template('qanda.html')

