import MySQLdb

db = MySQLdb.connect(host="localhost",    # host, usually localhost; IP address of the DB otherwise
                     user="admin",         # username
                     passwd="",  		  # password
                     db="registry")       # name of the database

# you must create a Cursor object. It will let
# you execute all the queries you need
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print "Database version : %s " % data


firstname = request.POST['firstname']
lastname = request.POST['lastname']
dateofbirth = request.POST['dob']
electiontype = request.POST['electiontype']
locality = request.POST['locality']

query = "SELECT * FROM user_table WHERE firstname='firstname' AND lastname='lastname' AND dateofbirth='dateofbirth' AND electiontype='electiontype' AND locality='locality'" # remember to change these values

cursor.execute(query)
#results = cursor.fetchall()

if cursor.rowcount > 0:
	# make second connection		TODO: Make 2nd DataBase; should be a Postgre MySQL db
	# db = MySQLdb.connect(host="localhost",user="admin",passwd="",db="voter_records")   # this is the "HasVoted" database
	# cursor = db.cursor()
	# query = "SELECT * FROM user_table WHERE firstname='firstname' AND lastname='lastname'"
	# cursor.execute(query)
	# if cursor.rowcount != 0
		# Move on to creating a Booth object and whatnot
		
	# else
		# redirect to page that says "already has voted"	
		# Location.localhost:8000/voted.html
else:
	# redirect to page that says "Not registered or re-enter"
	# Location:localhost:8000/re-checkin.html
	

# disconnect from server
db.close()