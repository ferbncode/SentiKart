import pickle#This file contains the basic content management system which judges what content is seen in the html pages
def Content():
	file1 = open('conman','rb')
	DICT = pickle.load(file1)
	return DICT
def Database():
	file2 = open('dbbase','rb')
	DB = pickle.load(file2)
	return DB
def Write_Cont(CONT_DICT):
	file1 = open('conman', 'wb')
	file1.dump(CONT_DICT, file1, protocol=2)
	file1.close()
def Write_DB(DB):
	file2 = open('dbbase', 'wb')
	file2.dump(DB, file2, protocol=2)
	file2.close()

	
