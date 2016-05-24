#module for the application
from __future__ import division
import pickle 
from datetime import datetime,timedelta
from content_management import Content, Database, Write_Cont, Write_DB


CAT_DICT = {'Serv':'Service','Looks':'Looks','Cam':'Camera','Vfm':'Value for Money','Disp':'Display','perf':'Performance', 'Serv':'Service','Perf':'Performance', 'Cam':'Camera','OverAll':'OverAll', 'Bat':'Battery', 'Look':'Look', 'Camera':'Camera' }

def _openFile(filename):
	
	fileObj = open(filename,'rb')
	bigList = pickle.load(fileObj)
	return bigList

def _prepareDateList(bigList):

	dateList = [0]
	for element in range(len(bigList)):
		date = bigList[element][0].encode()
		date = date.split('-')
		epoch = datetime.datetime.utcfromtimestamp(0)
		for i in range(len(date)):
			date[i] = int(date[i])
		dt = datetime.datetime(date[0],date[1],date[2])
		var = (dt - epoch).total_seconds() * 1000.0
		if (dateList[-1]!=var):
			dateList.append(var)
	return dateList

def _prepareCategoryList(bigList):
	'''This function would return the overall sentiment of the whole situation (categorywise) but would not return it return datewise'''
	element1 = bigList[0][1]
	categoryList = list(element1.keys())
	noOfCategories = len(categoryList)
	categoryListFinale = {}
	for category in categoryList:
		categoryListFinale[category] = []
	datelist = [0]
	Overall_sentiment=0
	length = 0
	for element in range(len(bigList)):
		myDict = bigList[element][1]
		date = bigList[element][0]
		date = date.split('-')
		epoch =datetime.utcfromtimestamp(0)
		for i in range(len(date)):
			date[i] = int(date[i])
		dt = datetime(date[0],date[1],date[2])
		td = (dt - epoch)
		td = (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**3

		for category in categoryList:
			sentimentValue = myDict[category]
			if ((sentimentValue!=0)and(datelist[-1]!=td)):
				Overall_sentiment = Overall_sentiment + sentimentValue
				categoryListFinale[category].append([td,sentimentValue])
				length = length + 1
				datelist.append(td)
	Overall_sentiment = Overall_sentiment/length
	return (categoryList, categoryListFinale,Overall_sentiment)

def _url_update(categoryList, productname, filename):
	dict1 = Content()
	dict2 = Database()
	categoryList = list(categoryList)
	a = []
	for i in range(len(categoryList)):
		a.append(CAT_DICT[categoryList[i]])
	dict1[productname]=[]

def _check(filename):
	bigList = _openFile(filename)
	categoryList,categoryListFinale,Overall_sentiment = _prepareCategoryList(bigList)
	a = categoryListFinale
	print (a)
	return a

		
def _prepareCategoryList2(bigList):
	'''This function would return the overall sentiment of the whole situation (categorywise) but would not return it return datewise'''
	element1 = bigList[0][1]
	categoryList = list(element1.keys())
	noOfCategories = len(categoryList)
	categoryListFinale = {}
	for category in categoryList:
		categoryListFinale[category] = [0,0]
	datelist = [0]
	Overall_sentiment=0
	length = 0
	for element in range(len(bigList)):
		myDict = bigList[element][1]
		date = bigList[element][0]
		date = date.split('-')
		epoch =datetime.utcfromtimestamp(0)
		for i in range(len(date)):
			date[i] = int(date[i])
		dt = datetime(date[0],date[1],date[2])
		td = (dt - epoch)
		td = (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**3

		for category in categoryList:
			sentimentValue = myDict[category]
			if ((sentimentValue!=0)):
				if (sentimentValue > 0 ):
					categoryListFinale[category][0]=categoryListFinale[category][0]+sentimentValue
				if (sentimentValue < 0):
					categoryListFinale[category][1]=categoryListFinale[category][1]+sentimentValue
	for category in categoryList:
		total = categoryListFinale[category][0] - categoryListFinale[category][1]
		categoryListFinale[category][0] = categoryListFinale[category][0]/total *100.0
		categoryListFinale[category][1] = 0 - categoryListFinale[category][1]/total*100.0
	return categoryListFinale


def _pie(filename):
	bigList = _openFile(filename)
	categoryListFinale = _prepareCategoryList2(bigList)
	return categoryListFinale
