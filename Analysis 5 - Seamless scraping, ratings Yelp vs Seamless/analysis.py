import pandas as pd
from dbconnection import connect_to_db

def analyze_yelp_seamless():
	
	# call connect_to_db to setup a connection to the db
	conn, curr = connect_to_db('8889', 'root', 'root', 'USE YELP_DATA_PROJECT')

	# uncomment below code if you need to get a clean print of the pandas data frame
	# pd.set_option('display.height', 1000)
	# pd.set_option('display.max_rows', 500)
	# pd.set_option('display.max_columns', 500)
	# pd.set_option('display.width', 1000)

	# query to extract all yelp restaurants from db
	yelp_query = 'SELECT zip_code, name, stars, review_count, state FROM usa_businesses;'
	# query to extract all scraped seamless restaurants from db
	seamless_query = 'SELECT zip_code, name, stars, review_count FROM seamless_data;'

	# create pandas data frames for yelp and seamless restaurants in the db
	yelp_data_frame = pd.read_sql(yelp_query, conn)
	seamless_data_frame = pd.read_sql(seamless_query, conn)
	
	# inner join the two dataframes matching on zipcode and restaurant name
	merged_data_frame = pd.merge(seamless_data_frame, yelp_data_frame, how = 'inner', on = ['zip_code', 'name'])
	# merged columns: x -> seamless data, y -> yelp data
	
	# get the absolute difference between ratings and review count
	merged_data_frame['delta_stars'] = abs(merged_data_frame['stars_x'] - merged_data_frame['stars_y'])
	merged_data_frame['delta_reviews'] = abs(merged_data_frame['review_count_x'] - merged_data_frame['review_count_y'])
	
	return merged_data_frame
