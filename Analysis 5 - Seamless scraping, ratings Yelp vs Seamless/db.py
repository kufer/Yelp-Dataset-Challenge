import pymysql #Connector library for mysql
import json #library to read JSON

#Set up a connection with the server
conn = pymysql.connect(host = 'localhost', port = 8889, user = 'root', passwd = 'root')

#And a cursor object that will serve as a virtual 'cursor'
curr = conn.cursor()
curr.execute('CREATE DATABASE IF NOT EXISTS YELP_DATA_PROJECT;')
curr.execute('USE YELP_DATA_PROJECT')

#create a table for users and populate it with values from the users JSON
curr.execute('CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(35), yelping_since VARCHAR(10), votes VARCHAR(500), review_count INTEGER, name VARCHAR(100), friends VARCHAR(60000), fans INTEGER, average_stars FLOAT, type VARCHAR(50), compliments VARCHAR(1000), elite VARCHAR(100), PRIMARY KEY (user_id));')
datafile = 'yelp_academic_dataset_user.json'
with open(datafile, 'r') as f:
    
    count = 1 #count of records 
    failures = [] # list of record read failures 
    
    for line in f:
        
        data = json.loads(line)

        # all the parameters of the users
        yelping_since = data.get('yelping_since')
        votes = data.get('votes')
        review_count = data.get('review_count')
        name = data.get('name')
        user_id = data.get('user_id')
        friends = data.get('friends')
        fans = data.get('fans')
        average_stars = data.get('average_stars')
        type_data = data.get('type')
        compliments = data.get('compliments')
        elite = data.get('elite')
        
        # Prepare the data to be inserted
        data_string = '"' + user_id + '","' + yelping_since + '","' + str(votes) + '","' + str(review_count)+ '","' + "u"  + str(name) + '","' + str(friends) + '","' + str(fans) + '","' + str(average_stars) + '","' + type_data + '","' + str(compliments) + '","' + str(elite) + '"'
        user_query = 'INSERT INTO users VALUES ('+data_string+')'
        
        try:
            curr.execute(user_query)
            conn.commit()
        except:
            failures.append(count)
            continue
            
        count += 1

print("Following records failed to insert into table users: ", failures)
print("No. of lost records: ", len(failures))
f.close()

#create a table for tips and populate it with values from the tips JSON
curr.execute('CREATE TABLE IF NOT EXISTS tips (business_id VARCHAR(35), user_id VARCHAR(35), text VARCHAR(500), likes INTEGER, date DATE, type VARCHAR(15));')
datafile = 'yelp_academic_dataset_tip.json'
with open(datafile,'r') as f:
    
    count = 1 #count of records 
    failures = [] # list of record read failures 

    for line in f:
        
        data = json.loads(line)

        # all the parameters of the tips
        business_id = data.get('business_id')
        user_id = data.get('user_id')
        text = data.get('text')
        likes = data.get('likes')
        date = data.get('date')
        type_data=data.get('type')
        
        #fix text for MySQL insert
        text = str(text)
        text = text.replace('"','')
        text = text.replace("'","")
        
        # Prepare the data to be inserted
        data_string = '"' + str(business_id) + '","' + str(user_id) + '","' + str(text) + '","' + str(likes) + '","' + str(date) + '","' + str(type_data) + '"'
        user_query = 'INSERT INTO tips VALUES ('+data_string+')'
        
        try:
            curr.execute(user_query)
            conn.commit()
        except:
            failures.append(count)
            continue
            
        count += 1

print("Following records failed to insert into table tips: ", failures)
print("No. of lost records: ", len(failures))
f.close()

#create a table for reviews and populate it with values from the reviews JSON
curr.execute('CREATE TABLE IF NOT EXISTS reviews (review_id VARCHAR(35), user_id VARCHAR(35), business_id VARCHAR(35), date DATE, text VARCHAR(8000), votes VARCHAR(40), stars FLOAT, type VARCHAR(10), PRIMARY KEY (review_id));') 
datafile = 'yelp_academic_dataset_review.json'
with open(datafile,'r') as f:
    
    count = 1 #count of records 
    failures = [] # list of record read failures 

    for line in f:
        
        data = json.loads(line)
       
        # all the parameters of the reviews
        votes = data.get('votes')
        user_id = data.get('user_id')
        review_id = data.get('review_id')
        stars = data.get('stars')
        date = data.get('date')
        text = data.get('text')
        type_data = data.get('type')
        business_id = data.get('business_id')
        
        #fix text for MySQL insert
        text = str(text)
        text = text.replace('"','')

        # Prepare the data to be inserted
        data_string = '"' + str(review_id) + '","' + str(user_id) + '","' + str(business_id) + '","' + str(date) + '","' + str(text) + '","' + str(votes) + '","' + str(stars) + '","' + str(type_data) + '"'
        user_query = 'INSERT INTO reviews VALUES ('+data_string+')'
        
        try:
            curr.execute(user_query)
            conn.commit()
        except:
            failures.append(count)
            continue
            
        count += 1

print("Following records failed to insert into table reviews: ", failures)
print("No. of lost records: ", len(failures))
f.close()

#create a table for checkins and populate it with values from the checkins JSON
curr.execute('CREATE TABLE IF NOT EXISTS checkins (business_id VARCHAR(35), checkin_info VARCHAR(5000), type VARCHAR(15), PRIMARY KEY(business_id));')
datafile = 'yelp_academic_dataset_checkin.json'
with open(datafile,'r') as f:
    
	count = 1 #count of records
	failures = [] #list of record read failures 

	for line in f:
        
		data = json.loads(line)

        # all the parameters of the checkin
		business_id = data.get('business_id')
		checkin_info = data.get('checkin_info')
		type_data = data.get('type')
        
        # Prepare the data to be inserted
		data_string = '"' + business_id + '","' + str(checkin_info) + '","' + type_data + '"'
		user_query = 'INSERT INTO checkins VALUES ('+data_string+')'
        
		try:
			curr.execute(user_query)
			conn.commit()
		except:
			failures.append(count)
			continue
            
		count += 1

print("Following records failed to insert into table checkins: ", failures)
print("No. of lost records: ", len(failures))
f.close()

#create a table for businesses and populate it with values from the businesses JSON
curr.execute('CREATE TABLE IF NOT EXISTS businesses (business_id VARCHAR(35), zip_code VARCHAR(5), full_address VARCHAR(500), hours VARCHAR(500), open BOOLEAN, categories VARCHAR(400), city VARCHAR(100), review_count INTEGER, name VARCHAR(200), neighborhoods VARCHAR(400), longitude FLOAT, state VARCHAR(10), stars REAL, latitude FLOAT, attributes VARCHAR(3000), type VARCHAR(15), PRIMARY KEY (business_id));')
datafile = 'yelp_academic_dataset_business.json'
with open(datafile,'r') as f:
    
	count = 1 #count of records 
	failures = [] # list of record read failures

	for line in f:

		data = json.loads(line)

        # all the parameters of the businesses
		business_id = data.get('business_id')
		full_address = data.get('full_address')
		hours = data.get('hours')
		open_data = data.get('open')
		categories = data.get('categories')
		city = data.get('city')
		review_count = data.get('review_count')
		name = data.get('name')
		neighborhoods = data.get('neighborhoods')
		longitude = data.get('longitude')
		state = data.get('state')
		stars = data.get('stars')
		latitude = data.get('latitude')
		attributes = data.get('attributes')
		type_data = data.get('type')

        #Fix the apostrophe in categories
		categories = str(categories)
		categories = categories.replace('"','')
		neighborhoods = str(neighborhoods)
		neighborhoods = neighborhoods.replace('"','')

		# get business zipcode as last 5 characters of the address
		zip_code = full_address[-5:]

		# Prepare the data to be inserted
		data_string = '"' + business_id + '","' + str(zip_code) + '","' + str(full_address) + '","' + str(hours) + '",' + str(open_data) + ',"' + str(categories) + '","' + city + '","' + str(review_count) + '","' + name + '","' + str(neighborhoods) + '","' + str(longitude) + '","' + state + '","' + str(stars)+ '","' + str(latitude) + '","' + str(attributes) + '","' + type_data + '"'
		user_query = 'INSERT INTO businesses VALUES ('+data_string+')'

		try:
		    curr.execute(user_query)
		    conn.commit()
		except:
		    failures.append(count)
		    continue
		    
		count += 1

print("Following records failed to insert into table businesses: ", failures)
print("No. of lost records: ", len(failures))
f.close()

#create tables for USA and restaurants only from the master tables of businesses, reviews, tips, checkins
curr.execute('CREATE TABLE IF NOT EXISTS usa_businesses (business_id VARCHAR(35), zip_code VARCHAR(5), full_address VARCHAR(500), hours VARCHAR(500), open BOOLEAN, categories VARCHAR(400), city VARCHAR(100), review_count INTEGER, name VARCHAR(200), neighborhoods VARCHAR(400), longitude FLOAT, state VARCHAR(10), stars REAL, latitude FLOAT, attributes VARCHAR(3000), type VARCHAR(15), PRIMARY KEY (business_id))')
states = ['PA','NC','IL','WI','AZ','NV']
arg = "%" + "Restaurants" + "%"
query = ('INSERT INTO usa_businesses SELECT * FROM businesses WHERE categories LIKE %s AND state IN %s')
try:
    curr.execute(query, (arg, tuple(states)))
    conn.commit()
except:
    print("Error creating table usa_businesses")

curr.execute('CREATE TABLE IF NOT EXISTS usa_tips (business_id VARCHAR(35), user_id VARCHAR(35), text VARCHAR(500), likes INTEGER, date DATE, type VARCHAR(15));')
query = ('INSERT INTO usa_tips SELECT * FROM tips WHERE business_id IN(SELECT business_id FROM usa_businesses)')
try:
    curr.execute(query)
    conn.commit()
except:
 	print("Error creating table usa_tips")

curr.execute('CREATE TABLE IF NOT EXISTS usa_checkins (business_id VARCHAR(35), checkin_info VARCHAR(5000), type VARCHAR(15), PRIMARY KEY(business_id));')
query = ('INSERT INTO usa_checkins SELECT * FROM checkins WHERE business_id IN(SELECT business_id FROM usa_businesses)')
try:
    curr.execute(query)
    conn.commit()
except:
	print("Error creating table usa_checkins")

curr.execute('CREATE TABLE IF NOT EXISTS usa_reviews (review_id VARCHAR(35), user_id VARCHAR(35), business_id VARCHAR(35), date DATE, text VARCHAR(8000), votes VARCHAR(40), stars FLOAT, type VARCHAR(10), PRIMARY KEY (review_id));')
query = ('INSERT INTO usa_reviews SELECT * FROM reviews WHERE business_id IN(SELECT business_id FROM usa_businesses)')
try:
    curr.execute(query)
    conn.commit()
except:
	print("Error creating table usa_reviews")
	








