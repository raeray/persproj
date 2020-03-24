from flask import Flask, render_template, url_for, request, redirect,jsonify
import pandas as pd
from settings import Settings
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
from flask_pymongo import MongoClient

# app.config["MONGO_URI"] = "mongodb://localhost:27017/Tags.Corpus"
# mongo = PyMongo(app)

#################################################
# HARD CODED CONSTANTS
#################################################

client = MongoClient('mongodb://127.0.0.1:27017')
settings = Settings()
db_geo = client.get_database(settings.GEO_DATABASE)
collection_reviews = db_geo.get_collection(settings.REVIEW_COLLECTION)
collection_topics = db_geo.get_collection(settings.TOPIC_COLLECTION)

db_business = client.get_database(settings.BUSINESS_DATABASE)
collection_business = db_business.get_collection(settings.BUSINESS_COLLECTION)

print('count', collection_business.count())


#################################################
# Geospatial query
#################################################

@app.route('/business_geo', methods=['GET'])
def get_business_geo_points():
	
	boundaries = json.loads(request.args.get('boundaries', ''))

	left_upper_bound = [boundaries.get('_southWest').get('lng'), boundaries.get('_northEast').get('lat')]
	right_upper_bound = [boundaries.get('_northEast').get('lng'), boundaries.get('_northEast').get('lat')]
	left_lower_bound = [boundaries.get('_southWest').get('lng'), boundaries.get('_southWest').get('lat')]
	right_lower_bound = [boundaries.get('_northEast').get('lng'),boundaries.get('_southWest').get('lat')]

	cursor = collection_business.find({'location': 
		{'$geoWithin':
			{'$geometry':
				{'type': "Polygon",
				'coordinates': [[
								left_upper_bound,
								right_upper_bound,
								right_lower_bound,
								left_lower_bound,
								left_upper_bound]]
								}
				}
			}
		}
	)

	cursor_list = [x for x in cursor]
	
	points = []
	iter_ = 0
	for item in cursor_list:
		points.append({
			"name": item['name'],
			"type": "Feature",
			"business_id": item['business_id'],
			"review_count": item['review_count'],
			"business_stars": item['stars'],
			"geometry": {
				"type": item['location']['type'],
				"coordinates": [item['location']['coordinates'][0],item['location']['coordinates'][1]]
			}
		})
		iter_ += 1
		# no more than 100 markers
		if iter_ > 100:
			break

	print('points len', len(points))

	return jsonify(points)

@app.route('/review', methods=['GET'])
def get_business_reviews():
	business_id = request.args.get('business_id')

	# get list of reviews for the business
	cursor = collection_reviews.find({'business': business_id})

	cursor_list = [x for x in cursor]
	
	reviews = []
	iter_ = 0
	for item in cursor_list:
		reviews.append({
					'reviewId': item['reviewId'],
					'text': item['text'],
					'cool': item['cool'],
					'date': item['date'],
					'funny': item['funny'],
					'review_stars': item['review_stars'],
					'useful': item['useful'],
					# 'geometry': {
					# 	"type": item['location']['type'],
					# 	"coordinates": [item['location']['coordinates'][0],item['location']['coordinates'][1]]
					# }
				})

		iter_ += 1
		
		# no more than 30 reviews
		if iter_ > 30:
			break
	return jsonify(reviews)

@app.route('/topics', methods=['GET'])
def get_topics_distribution():
	print('calls to python function')

	# get list of reviews for the business
	business_id = request.args.get('business_id')


	# get list of reviews for the business
	cursor = collection_topics.find({'business': business_id})

	def add_value_or_not(value, l):
		if value != None:
			l.append(float(value))
			return l
		else:
			return l

	topic0=[]
	topic1=[]
	topic2=[]
	topic3=[]
	topic4=[]
	topic5=[]
	topic6=[]
	topic7=[]
	topic8=[]
	topic9=[]
	topic10=[]
	topic11=[]
	topic12=[]
	
	sum_calcs = {}
	for review in cursor:
		sum_calcs = {
		'topic0': add_value_or_not(review['topics'].get('0'), topic0),
		'topic1': add_value_or_not(review['topics'].get('1'), topic1),
		'topic2': add_value_or_not(review['topics'].get('2'), topic2),
		'topic3': add_value_or_not(review['topics'].get('3'), topic3),
		'topic4': add_value_or_not(review['topics'].get('4'), topic4),
		'topic5': add_value_or_not(review['topics'].get('5'), topic5),
		'topic6': add_value_or_not(review['topics'].get('6'), topic6),
		'topic7': add_value_or_not(review['topics'].get('7'), topic7),
		'topic8': add_value_or_not(review['topics'].get('8'), topic8),
		'topic9': add_value_or_not(review['topics'].get('9'), topic9),
		'topic10': add_value_or_not(review['topics'].get('10'), topic10),
		'topic11': add_value_or_not(review['topics'].get('11'), topic11),
		'topic12': add_value_or_not(review['topics'].get('12'), topic12)
		}


	# calculate average of each topic
	return jsonify([sum(x[1])/len(x[1]) for x in sum_calcs.items()])
	

#################################################
# Yelp Fushio API Setup
# source : https://github.com/Pyligent/Business-Analytics-Platform
#################################################


API_KEY= settings.YELP_FUSION_API_KEY
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Default values.
DEFAULT_TERM = 'bars'
DEFAULT_LOCATION = 'Toronto'
SEARCH_LIMIT = 5


# def request(host, path, api_key, url_params=None):
#     """Given your API_KEY, send a GET request to the API.

#     Args:
#         host (str): The domain host of the API.
#         path (str): The path of the API after the domain.
#         API_KEY (str): Your API Key.
#         url_params (dict): An optional set of query parameters in the request.

#     Returns:
#         dict: The JSON response from the request.

#     Raises:
#         HTTPError: An error occurs from the HTTP request.
#     """
#     url_params = url_params or {}
#     url = '{0}{1}'.format(host, quote(path.encode('utf8')))
#     headers = {
#         'Authorization': 'Bearer %s' % api_key,
#     }

#     print(u'Querying {0} ...'.format(url))
	
#     response = requests.request('GET', url, headers=headers, params=url_params)

#     return response.json()


def search(api_key, term, location):
	"""Query the Search API by a search term and location.

	Args:
		term (str): The search term passed to the API.
		location (str): The search location passed to the API.

	Returns:
		dict: The JSON response from the request.
	"""

	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit':50
		   }
	print(url_params)
	return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
	"""Query the Business API by a business ID.

	Args:
		business_id (str): The ID of the business to query.

	Returns:
		dict: The JSON response from the request.
	"""
	business_path = BUSINESS_PATH + business_id

	return request(API_HOST, business_path, api_key)

@app.route('/')
def index():
	if display_review_table():
		review_list = 'thingy'
		# display_review_table()
		print('index template found review',review_list)

	return render_template("index.html", review_list = review_list)        

@app.route("/search")
def search():
	return render_template("search.html")

@app.route("/explore")
def explore():
	return render_template("explore.html")

if __name__ == '__main__':
	app.run(debug=True)

