import sqlite3
'''Integratiing sentiment value with the answers and printing the result within the browser is to be done. Moreover, the askexpert button need to be added'''
conn = sqlite3.connect('qanda.db')
c = conn.cursor()
def createdb():
	c.execute("CREATE TABLE IF NOT EXISTS qanda(askuser TEXT, question TEXT, description TEXT, answers TEXT, useranswers TEXT, sentiment REAL)")
def createQuestionEntry(askingUsr, Question, Description):
	c.execute("INSERT INTO qanda(askuser, question, description) VALUES (?,?,?)", (askingUsr, Question, Description))
	conn.commit()

def addNewAnswer(ansUser, Question, Answer):
	c.execute("SELECT useranswers FROM qanda WHERE question='{}'".format(Question))
	a = c.fetchall()
	acheck = [(None,) for i in range(len(a))]
	if acheck == a:
		a = []
		a.append(ansUser)
		c.execute("""UPDATE qanda SET useranswers = ? WHERE question =?""",(str(a), Question))
		theanswers = []
		theanswers.append(Answer)
		c.execute("""UPDATE qanda SET answers = ? WHERE question = ?""",(str(theanswers), Question))
		conn.commit()
	else:
		#this is not the first answer
		import ast
		a = ast.literal_eval(a[0][0])
		a.append(ansUser)
		c.execute("SELECT answers FROM qanda WHERE question='{}'".format(Question))
		theanswers = c.fetchall()
		theanswers = ast.literal_eval(theanswers[0][0])
		theanswers.append(Answer)
		c.execute("""UPDATE qanda SET answers = ? WHERE question=?""", (str(theanswers), Question))
		c.execute("""UPDATE qanda SET useranswers = ? WHERE question =?""",(str(a), Question))
		conn.commit()	
def returnWholeData():
	c.execute("SELECT * FROM qanda WHERE answers is not null")
	a = c.fetchall()
	return a
def returnUnanswered():
	c.execute("SELECT * FROM qanda WHERE answers is null")
	a = c.fetchall()
	return a
