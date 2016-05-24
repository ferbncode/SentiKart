
import forms
from flask import Flask,render_template,url_for,request,redirect,flash
import datetime
import read_database
app = Flask(__name__)
from content_management import Content,Database, Write_Cont, Write_DB 
from services_content_management import services_content, mall_content
from flask.ext.login import *
CONT_DICT = Content()
SERV_DICT = services_content()
MALL_DICT = mall_content()
app.secret_key = 'sdkjfjkja'
DATABASE_DICT = Database()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html') 
global product
@app.route('/product')
def product():
	"""
	Controls the coming of the graph on the first search and of course the subsequent ones.
	The product being searched comes via here

	"""
	product=request.args['product']
	return redirect("/trend/{}_OverAll".format(product))
@app.route('/main_product', methods=['GET','POST'])
def main_product():
	if request.method == 'POST':
		product_name = request.form['productname']
		import createproductdb
		createproductdb.c.execute("SELECT * FROM products WHERE productname='{}'".format(product_name))
		x = createproductdb.c.fetchall()
		if (len(x)!=0):
			return redirect("trend/{}_OverAll".format(product_name))
		return redirect("/wearedoing/{}".format(product_name))
	return render_template("product.html")
@app.route('/profile')
def fc():
	return render_template('user_profile.html')
@app.route('/wearedoing/<productname>')
def wearedoingit(productname):
	#doing the naive bayes thing here
	return render_template("wearedoingit.html", productname = productname)

@app.route('/trend/<product>')
def product_Overall(product,chartID = 'chart_ID2',chart_type = 'line', chart_height = 500):
	"""
	Controls the coming of the graph on the first search and of course the subsequent ones.
	The product being searched comes via here

	"""
	product_list = product.split('_')
	product_name = product_list[0]
	import createproductdb
	createproductdb.c.execute("SELECT trust FROM products WHERE productname='{}'".format(product_name))
	x = createproductdb.c.fetchall()
	trust_value = x[0][0]
	database = DATABASE_DICT[product_name]
	category = product_list[1]
	product_dict = read_database._check(database)
	data = product_dict[category]
	length_of_product = len(CONT_DICT[product_name])
	title = {"text":"Overall Sentiment"}
	chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
	series = [{"type":"line", "name":"OverAll Sentiment" , "data":data}]
	pageType = 'areachart'
	return render_template('graph.html',pageType = pageType,length_of_product = length_of_product, chart = chart, chartID = chartID, title = title, series = series,product_name =product_name ,CONT_DICT = CONT_DICT, trust_value = trust_value)


@app.route('/<product>')
def addon(product):
	'''This function is a plugin that can be used to open sentikart from fiipkart product page.'''
	product_name = product
	import createproductdb
	createproductdb.c.execute("SELECT * FROM products WHERE productname='{}'".format(product_name))
	x = createproductdb.c.fetchall()
	if(len(x)!=0):
		return redirect('trend/{}_OverAll'.format(product_name))
	return redirect("/wearedoing/{}".format(product_name))
#@app.route('/product/daily')
#def product2(chartID = 'chart_ID2',chart_type = 'line', chart_height = 500,product = product):
	"""
	Controls the coming of the graph on the first search and of course the subsequent ones.
	The product being searched comes via here

	"""
#        category = "OverAll"
#        product_dict = read_database._daily(database)
#        data = product_dict[category]
#        title = {"text":"Overall Sentiment"}
#        chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
#        series = [{"type":"line", "name":"OverAll Sentiment" , "data":data}]
#        pageType = 'areachart'
#        return render_template('graph.html',pageType = pageType, chart = chart, chartID = chartID, title = title, series = series,product=product)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404


@app.route('/graph')
def graph(chartID = 'chart_ID',chart_type = 'bar',chart_height = 500):
	# WORK IS LEFT
	sentiment = dictionaryTest.main()
	pageType = 'graph2'
	chart = {"renderTo":chartID, "type": chart_type,"height": chart_height, "zoomType":'x'}
	series = [{"name":'Label1',"data":[1,2,3]},{"name":'Label2',"data":[3,4,5]}]
	graphtitle = {"text":'Product Summary'}
	xAxis = {"categories":['Service','Overall Features','Camera']}
	yAxis = {"title":{"text":'This is a test graph'}}
	title = {"text":'Product Summary(GRAPH)'}
	return render_template('graph.html',pageType = pageType, chart=chart,chartID=chartID,title = title, series = series,graphtitle = graphtitle, xAxis = xAxis,yAxis = yAxis)



#@app.route('/performance')
#def graph_line(chartID = 'chart_ID2',chart_type = 'line', chart_height = 500):
#        pageType = 'graph2'
#        chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
#        dataset = []
#        dataset2 = [2,3,2,4,2,1,3,2,1,-23]
#        series = [{"name":'LOOKS',"data":dataset},{"name":'SERVICE',"data":dataset2}]
#        xAxis = {"type":"datetime"}
#        yAxis = {"text":'Product Summary(GRAPH)'}
#        title = {"text":'Product Overall Graph'}
#	return render_template('graph.html',pageType = pageType, chart = chart, chartID = chartID, title = title, series = series,xAxis=xAxis,yAxis=yAxis)

@app.route('/piechart/<product>')
def pie_chart(product,chartID = 'chart_ID', chart_type = 'pie',chart_height = 500):
		# This is to be worked out
	product_list = product.split('_')
	product_name = product_list[0]
	analysis_category = product_list[1]
	pageType = 'piechart'
	chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
	data_dict = read_database._pie(DATABASE_DICT[product_name])
	data1 = data_dict[analysis_category][0]
	length_of_product = len(CONT_DICT[product_name])
	data2 = data_dict[analysis_category][1]
	data2 = [{"name":"Positive Sentiment","y" : data1},{"name":"Negative Sentiment","y":data2}]
	series = [{"name" : "Sentiment", "colorpoint":"true", "data":data2}]
	title = {"text":'Product {} graph  - Pie chart'.format(product_name)}
	return render_template('graph.html',pageType = pageType,length_of_product = length_of_product, chart = chart, chartID = chartID, title = title, series = series,product_name = product_name,CONT_DICT = CONT_DICT)

@app.route('/areagraph')
def area_graph(chartID = "chart_ID" , chart_type = 'line', chart_height = 500):
	pageType = 'areachart'
	category = 'OverAll'
	a = read_database._check('sentiment_redmi')
	import json
	data = json.dumps(a[category])
	data = a[category]
	title = {"text":"This is a test graph "}
	chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
	series = [{"type":"line", "name":"OverAll Sentiment" , "data":data}]
	return render_template('graph.html',pageType = pageType, chart = chart, chartID = chartID, series = series, title = title) 

@app.route('/qanda')
def mainpage():

	import createqandadb
	import ast
	queslist = createqandadb.returnWholeData()
	for i in range(len(queslist)):
		queslist[i] = list(queslist[i])
		anslist = ast.literal_eval(queslist[i][3])
		queslist[i][3] = anslist
		ansuser = ast.literal_eval(queslist[i][4])
		queslist[i][4] = ansuser
	return render_template('qanda.html', queslist=queslist)
@app.route('/newquestion', methods=["GET","POST"])
def question_page():
	import createqandadb
	if request.method == 'POST':
		mainquery = request.form['MainQuest']
		description = request.form['description']
		createqandadb.createQuestionEntry("BimalKant Lauhny", mainquery, description)
		if mainquery!='':
			return redirect('/answer_question')
	return render_template('newquestion.html')
@app.route('/answer_question')
def answer_page():
	import createqandadb 
	Unanswered = createqandadb.returnUnanswered()
	return render_template('ansaques.html', Unanswered = Unanswered)
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/services')
def services():
	pageType = "normal"
	return render_template('services.html', pageType=pageType, SERV_DICT = SERV_DICT, MALL_DICT = MALL_DICT)
@app.route('/services/<product>')
def services_product(product):
	pageType = "product"
	qproduct = product
	if qproduct in SERV_DICT.keys():
		database = SERV_DICT[qproduct]
	else:
		database = MALL_DICT[qproduct]
		return render_template('services.html', pageType=pageType, SERV_DICT=SERV_DICT, product = product, MALL_DICT=MALL_DICT)
		pageType = 'areachart'
		category = 'OverAll'
		a = read_database._check('sentiment_redmi')
		import json
		data = json.dumps(a[category])
		data = a[category]
		title = {"text":"This is a test graph "}
		chart = {"renderTo":chartID,"type": chart_type, "height":chart_height,"zoomType":'x'}
		series = [{"type":"line", "name":"OverAll Sentiment" , "data":data}]
		return render_template('graph.html',pageType = pageType, chart = chart, chartID = chartID, series = series, title = title) 

@app.route('/qanda')
def main_page():
	return render_template('qanda.html')


if __name__=='__main__':
	app.run(debug=True,port=8080,host='0.0.0.0',passthrough_errors=True)
