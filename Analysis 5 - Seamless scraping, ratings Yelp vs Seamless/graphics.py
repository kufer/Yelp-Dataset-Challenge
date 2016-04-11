import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def display_histo(data_frame):

	# plots a histogram of the dfifference betwen Yelp and Seamless ratings for restaurants 
	# Method 1 uses Plotly API
	# Method 2 uses matplotlib

	# Method 1
	# data = [go.Histogram(x = data_frame['delta_stars'], opacity = 0.75)]
	# layout = go.Layout(title = 'Rating Difference between Seamless and Yelp', xaxis = dict(title = 'Rating Difference'), yaxis = dict(title = 'Count'))
	# fig = go.Figure(data = data, layout = layout)
	# plot_url = py.plot(fig, filename = 'histo')

	#Method 2
	plt.hist(data_frame['delta_stars'], bins = 6)
	plt.title("Rating Difference between Seamless and Yelp")
	plt.xlabel("Rating Difference")
	plt.ylabel("Count")
	plt.show()

	return