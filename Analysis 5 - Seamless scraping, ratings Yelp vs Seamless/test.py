import pandas as pd
from scraper import seamless_web_scraper
from locations import get_locations
from dbconnection import connect_to_db
from analysis import analyze_yelp_seamless
from graphics import display_histo

failed = [] # data structure to contain thos scraped restaurants that could not be loaded to the db 
locations = [] # list of locations of yelp restaurants from the db that are used to scrape seamless

# call connect_to_db to setup a connection to the db, create a table for scraped seamless data
conn, curr = connect_to_db('8889', 'root', 'root', 'USE YELP_DATA_PROJECT')
curr.execute('CREATE TABLE IF NOT EXISTS seamless_data (zip_code VARCHAR(5), name VARCHAR(200), stars INTEGER, review_count INTEGER, review VARCHAR(60000), PRIMARY KEY (zip_code, name));')

# locations = get_locations()

# for loc in locations:
#  	failed.append(seamless_web_scraper(loc[0], conn))

# print(failed)

# the below function compares scraped seamless restaurants from the db with telp restaurants from the db to find matches
# then it computes the difference between the ratings and number of reviews using pandas, and uses that data to plot a histogram
analyzed_data_frame = analyze_yelp_seamless()
display_histo(analyzed_data_frame)

# use pandas to get summery statistics
# print out summary statistics for different data points
print('-----------------------')
print('\nThe summary statistics for the difference in ratings\n')
print(analyzed_data_frame['delta_stars'].describe())
print('-----------------------')
print('\nThe summary statistics for the difference in number of reviews\n')
print(analyzed_data_frame['delta_reviews'].describe())
print('-----------------------')
print('\nThe summary statistics for ratings on Seamless\n')
print(analyzed_data_frame['stars_x'].describe())
print('-----------------------')
print('\nThe summary statistics for ratings on Yelp\n')
print(analyzed_data_frame['stars_y'].describe())
print('-----------------------')
print('\nThe summary statistics for number of reviews on Seamless\n')
print(analyzed_data_frame['review_count_x'].describe())
print('-----------------------')
print('\nThe summary statistics for number of reviews on Yelp\n')
print(analyzed_data_frame['review_count_y'].describe())
print('-----------------------')