import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

def createdb():
	c.execute("CREATE TABLE IF NOT EXISTS users(users TEXT, password TEXT, email TEXT, details TEXT, karma INT)")
def newuser(username, email, encryptpassword):
	c.execute("INSERT INTO users(users, password, email, details) VALUES (?,?,?)",(username, email, encryptpassword, "New User", 0))
	conn.commit()

