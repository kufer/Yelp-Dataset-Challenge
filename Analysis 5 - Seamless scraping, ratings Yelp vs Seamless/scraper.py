from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from dbconnection import connect_to_db
import time

# connect to the webpage using PhantomJS as the driver with selenium
# create 2 webdrivers, one for extracting restaurants from pages
# the second for opening the restaurant page to get its zipcode and reviews
driver1 = webdriver.PhantomJS(executable_path = '/Applications/phantomjs')
driver2 = webdriver.PhantomJS(executable_path = '/Applications/phantomjs')

# if a graphical browser is needed use below code and comment above
# path_to_chromedriver = '/Users/kushal/Desktop/chromedriver' # change path as needed
#driver1 = webdriver.Chrome(executable_path = path_to_chromedriver)
#driver2 = webdriver.Chrome(executable_path = path_to_chromedriver)


# below statement creates a window size so that element will be found when using PhantomJS, if not used an ElementNotVisible exception will be thrown
# not needed if using Chrome or Firefox, it justs makes the window bigger from default size
driver1.set_window_size(1400, 900)  
driver1.set_page_load_timeout(60) # give the page 60 secs to load
driver1.implicitly_wait(15)
driver2.set_window_size(1400, 900)  
driver2.set_page_load_timeout(60) # give the page 60 secs to load
driver2.implicitly_wait(15)

# call connect_to_db to setup a connection to the db
conn, curr = connect_to_db('8889', 'root', 'root', 'USE YELP_DATA_PROJECT')

def seamless_web_scraper(location, conn):
	
	# data structures to hold intermediate and final results
	location_restaurants = [] 
	restaurants = []
	page_restaurants = []
	restaurant_info = []
	failures = []
	none_restaurants = False 
	curr = conn.cursor()

	url = 'https://www.seamless.com/'
	driver1.get(url) # load above page url

	# wait till the search form is available
	element = WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ghs-start-order-new-address-input"]/div/input')))
	# clear contents of the form
	element.clear()
	# type in the loaction into the form
	element.send_keys(location)
	# wait till the submit button for the form is clickable. Once it is, click it => submit the form
	WebDriverWait(driver1, 15).until(EC.element_to_be_clickable((By.ID, 'ghs-startOrder-searchBtn'))).click()
	time.sleep(3) # wait so that the clicking/submitting action is completed
	
	# check if there are restaurants for the submitted zipcode, if there are none return
	try:
		WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-panel.search-no-results.notInMarket')))
	except:
		pass
	else:
		return

	# wait till the 'open now' filter is visible and clickable. Once it is, cick the 'x' to remove the filter
	try:
		WebDriverWait(driver1, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ghs-search-results-container"]/div[1]/div/ghs-facet-list/div/div[6]/div/div/label/a'))).click()
	except TimeoutException:
		pass
		
	time.sleep(3) # important step, wait so that the clicking/submitting action is completed

	# scrape the total number of pages containing restaurants for given location using xpath of the page element
	try:
		num_pages = WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ghs-search-results-container"]/div[2]/div/div/div/div[2]/div/div/div[2]/span[4]'))).text
	except TimeoutException:
		return

	location_url = driver1.current_url
	
	# if number of pages is just 1 then above element will be absent, therefore we manually set num_pages to 1
	if num_pages is '':
		num_pages = 1
	
	# loop through pages of restaurants
	for page in range(1, int(num_pages) + 1):
		page_url = location_url + '&pageNum=' + str(page) # appends the page number to the location url
		
		try:
			driver1.get(page_url) # load the page corresponding to above url
		except TimeoutException:
			continue

		# wait for the footer of the page to be visible. once it is visible, we know all the restaurant names are available to scrape
		try:
			WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.forkFooter-section.legal-container.s-col-xs-12')))
		except TimeoutException:
			continue
		
		# find all page elements that contain all information pertaining to each restaurant on that page
		page_restaurants = driver1.find_elements_by_class_name('searchResult')

		# loop through each element that contains restaurant info
		for index in range(len(page_restaurants)):
			restaurant_info = page_restaurants[index].text.split('\n') # split restaurant info into the various text fields
			
			# check which field contains the rating
			for field in restaurant_info:
				flag = False # flag to know whether restaurant has a rating or not
				if 'Ratings' in field:
					if 'Not Enough' in field: # if not enough ratings then set flag to true and break
						flag = True
						break
					else: # else assign field to rating
						rating = field
			
			if flag is True: # checks flag for restaurant 'not enough ratings'
				continue # if true, force next iteration of restaurant information
			else:
				restaurant_name = restaurant_info[0] # get restaurant name
				no_of_ratings = (rating.split( ))[0] # get number of ratings, stripping the text 'ratings' to get only numeric value
				no_of_stars = len(page_restaurants[index].find_elements_by_css_selector('i.icon-star.unclickable.x')) # get number of stars

				check_query = ('SELECT * FROM seamless_data WHERE name = %s AND stars = %s AND review_count = %s')
				#print((restaurant_name, no_of_stars, no_of_ratings))
				#print(curr.execute(check_query, (restaurant_name, no_of_stars, no_of_ratings)))

				if curr.execute(check_query, (restaurant_name, no_of_stars, no_of_ratings)):
					continue
				else:
					zip_code, reviews_text = review_and_zipcode(page_restaurants[index], location) # call function to get zipcode and review of restaurant
					data_string_1 = '"' + str(zip_code) + '","' + str(restaurant_name) + '","' + str(no_of_stars) + '","' + str(no_of_ratings) + '","' + str(reviews_text) + '"'
					data_string_2 = '"' + str(zip_code) + '","' + str(restaurant_name) + '","' + str(no_of_stars) + '","' + str(no_of_ratings) + '","' + '" "' + '"'
					data_query_1 = 'INSERT INTO seamless_data VALUES ('+data_string_1+')'
					data_query_2 = 'INSERT INTO seamless_data VALUES ('+data_string_2+')'
					
					try:
						curr.execute(data_query_1)
						conn.commit()
					except:
						try:
							curr.execute(data_query_2)
							conn.commit()
						except:
							failures.append((zip_code, restaurant_name, no_of_stars, no_of_ratings))
	return failures

# this function scrapes the zipcode and only the first page of reviews for a restaurant
def review_and_zipcode(restaurant_element, location):
	review_string = '' # initialize string
	# get the hyperlink for the restaurant in the page
	review_link = restaurant_element.find_element_by_css_selector('a.restaurant-name.s-link').get_attribute('href')
	# use the second driver to open the restaurant's homepage
	try:
		driver2.get(review_link)
	except TimeoutException:
		return location, " "

	time.sleep(3) # wait for 3 seconds so that the page loads
	# get the zipcode as the last 5 characters of the restaurant address string
	zipcode = (driver2.find_element_by_class_name('restaurantHeader-secondaryInfo--address').text)[-5:]
	# find the page elements that contain the reviews
	review_elements = driver2.find_elements_by_class_name('r-content')
	# loo through each review element extracting the review and appending it to a string
	for review in review_elements:
		review_string = review_string + review.text
	
	return zipcode, review_string

