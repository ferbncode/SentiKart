import sqlite3

conn = sqlite3.connect('product.db')
c = conn.cursor()

def createdb():
	c.execute("CREATE TABLE IF NOT EXISTS products(productname TEXT, trust REAL)")
def newuser(productname, trust):
	c.execute("INSERT INTO products(productname, trust) VALUES (?,?)",(productname, trust))
	conn.commit()
