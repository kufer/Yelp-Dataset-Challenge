import pymysql #Connector library for mysql

def connect_to_db(db_port, db_user, db_pwd, db_name):
	
	#Set up a connection with the server
	conn = pymysql.connect(host = 'localhost', port = int(db_port), user = db_user, passwd = db_pwd)
	#And a cursor object that will serve as a virtual 'cursor'
	curr = conn.cursor()
	curr.execute(db_name)
	# return connection and cursor objects

	return conn, curr