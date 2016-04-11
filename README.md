# Yelp-Dataset-Challenge

Our group decided to explore the Yelp Challenge dataset with a particular focus on US restaurants. A series

of analyses was conducted, and the US restaurants dataset was investigated from different perspectives,

with main regard to the tables usa_businesses and usa_reviews. Most packages covered in class were

used, such as nltk, numpy, pandas, matploblib, pymysql, and some other popular ones were also required:

sklearn, random, math, selenium, beautifulsoup, wordcloud, among others. This is the simplified structure

of the data used, after pulling all the data from the Yelp Challenge data set and filtering for US restaurants

only. An independent table contains data scraped from Seamless.

Analysis 1 - Summarizing long reviews

After looking at the average size of a Yelp review, we realized that users tend to write long reviews of 660

characters on average. Inspired by the length of a tweet, the cutoff to categorize a review as being long

was 150 characters. Reviews longer than 150 characters were then summarized. The first step was to

create a dictionary containing reviews related keywords. This dictionary was created by i) tokenizing the

reviews, ii) stemming the reviews, iii) removing the stop words, iv) POS tagging the words and keeping the

nouns only, v) the top 16 keywords were then kept in the dictionary.

Once the dictionary was ready, we could start summarizing the long reviews. First the length of a review

was checked. If longer than 150 characters, the review was stemmed. We defined important sentences

to be part of the summary if one or more of the following rules applied.

• They contained one of the keywords from the dictionary previously created

• They contained a capitalized word in the sentence

• They contained two or more exclamation points

Those sentences were chosen since the user would use such keywords or formatting in order to emphasize

his opinion about a restaurant. The usa_reviews table was used in order to complete this analysis and the

nltk package was also used to preprocess the data.

Analysis 2 - Yelp vs Seamless

In order to better understand the difference between the Seamless and Yelp reviews, we decided to check

the difference in topics discussed in each case. In order to be able to intuitively show the results to the

user, we decided to create a word cloud for each of the sources. These word clouds were created using

matpoltlib and wordcloud. In order to only have standardized and relevant words in the word cloud, the

reviews were preprocessed using nltk. The words were stemmed, stop words were removed and only

nouns were kept. The data used for the Yelp word cloud is from usa_reviews and for seamless from

seamless_data.

This analysis allowed us to see that users on the two different platforms judge the same restaurant on

some similar dimensions like food but also different ones. In the Yelp case, customer service and

experience are important factors while order and delivery is important for Seamless.

Analysis 3 - Words that drive positive and negative ratings

As a second analysis, the group wanted to investigate which words drive positive and negative ratings. In

order to do so, a 4-step process was executed: i) reviews data extraction and manipulation, ii)

preprocessing and features generation, iii) model fitting, and iv) feature importance. The first stage refers

to extracting from the database all reviews targeted to restaurants located in the US, manipulating them

in Python, and randomly selecting a train and a test sets (which had 5,000 observations each, for the sake

of computational efforts). In the second step, the reviews were preprocessed, and a bag of words with

500 predictors was generated. In the third phase, having the review rating (from 1 to 5) as the response

variable, linear regression, random forest and support vector machine (linear) were evaluated, and the

group decided to move on with linear regression given that fit results (RMSE, adjusted R-squared) were

similar and that this is a more comprehensible model. In the fourth step, regression coefficients were

analyzed, and the group plotted the top 10 words which drive positive and negative reviews. Some

examples for positive words are “delicious”, “excellent” and “favorite”, whereas negative words include

“bland”, “cold”, “slow” and interestingly “manager”.

Analysis 4 - Plotting restaurants rating for a specific cuisine in a city using heat maps.

As a third analysis, we wanted to do a visual application of the Yelp data set. The data used was the Yelp

restaurants for U.S. cities. The goal of this study was to plot all the restaurants of specific cuisine (ex:

“Chinese”, “Japanese”, “Italian”, ...) on a city map and get some insights from it, on the location, the

quality, etc. on what to eat and where to go. and the average rating of the restaurant. One of the

challenge was to find a map to plot on it. We first tried to use Basemap and to print on a city scale using the

[latitude, longitude] information, but the result was not successful at a city scale. Then we decided to crop

a google map and convert the [latitude, longitude] of the extreme corners (upper left and lower right) into

pixel length. Each restaurant was placed on the map as a dot using the same conversion of its [latitude,

longitude] into pixel. The color (1-1.5: red, 2-2.5: orange, 3-3.5: yellow, 4-4.5: green, 5: blue) of the

restaurant would reflect its average rating. By plotting several cuisines on a map of Las Vegas, we were

able to drawn some interesting insight and compare cuisine distribution and quality in a chosen city.

Analysis 5 - Have you ever wondered whether there is any difference in reviews for the same product

on different portals?

This analysis aims to determine if there is significant variance between the star ratings on Yelp and

Seamless for the same restaurant. For example, is the rating for ‘Alfredo’s Pizza’ on Yelp different from its

rating on Seamless? The motivation behind answering this question is the difference in nature of the

reviews on Yelp (reviews more about dining in restaurant - food, ambience, service, etc.) and Seamless

(reviews talk mainly about food and delivery). One explanation for the variance, if any, would be the

delivery service (Seamless) or the ambience (Yelp). To implement this analysis, we begin by using the

browser automation tool Selenium along with the invisible browser tool PhantomJS as the web driver. We

then get a list of restaurant zipcodes (~ 365 unique zips) from the Yelp database, and input these into the

Seamless website search box through the virtual browser. We validate that there are restaurants on

seamless for the particular zipcode, and then scrape each results page for the restaurant name, zipcode,

review count, star rating, and reviews, loading the information into the database table seamless_data. If

the restaurant has no star rating, we ignore it and move to the next one. We also check that the restaurant

as identified by its name and zip code is unique, as it might appear multiple times on seamless because

search on seamless is by the zipcode to which a restaurant delivers, not the zipcode of the restaurant itself

- giving room for duplication to occur. Furthermore, the review text might contain unicode formatting

which makes loading into SQL problematic. For such records, we load all other information except the

review text (~ 650 unique scraped restaurants). Now, we use pandas to inner join on restaurants and

zipcode the scraped seamless data with the data from the Yelp database. This gives us a table of

restaurants (~ 280 restaurants) with their star rating and review count on seamless and Yelp. We can now

compute the differences, summary statistics and plot a histogram of the difference in ratings. One

important consideration is that Yelp ratings are in increments of 0.5 whereas Seamless ratings are in

increments of 1. Therefore, a difference of 0.5 is quite common. If we disregard this difference, we can

see that there is no substantive variance between ratings on Yelp and Seamless. Indeed, as you will see in

the next analysis a word cloud for the reviews for the same restaurant on Yelp and Seamless shows great

similarity, in contrast to what was expected.
