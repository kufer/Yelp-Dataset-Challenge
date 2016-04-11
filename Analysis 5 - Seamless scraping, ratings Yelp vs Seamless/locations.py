from dbconnection import connect_to_db

def get_locations():

	# dictionary keyed on zipcode, with values of (zipcode, city, state)
	locations_by_zip = {} 
	# # data structure to store db query results
	locations = []

	# call connect_to_db to setup a connection to the db
	conn, curr = connect_to_db('8889', 'root', 'root', 'USE YELP_DATA_PROJECT')

	# send SQL query to extract zipcode, city and state from the db
	query = 'SELECT zip_code, city, state FROM usa_businesses;'
	curr.execute(query)
	conn.commit()
	
	# store the results of the query (tuples) in a list
	locations = curr.fetchall()

	# remove duplicate locations, checking for duplication by zipcode
	for zip_code, city, state in locations:
	    if zip_code not in locations_by_zip and zip_code.isdigit(): 
	        locations_by_zip[zip_code] = (zip_code, city, state)
	
	# return the sorted dictionary {zipcode: (zipcode, city, state)}
	return(sorted(locations_by_zip.items()))


