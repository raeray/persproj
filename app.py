from flask import Flask, render_template, url_for, request, redirect,jsonify
import os
import sys
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from settings import Settings
from predict import Predict
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

import requests
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


app = Flask(__name__)
from flask_pymongo import MongoClient
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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
collection_topic_values = db_geo.get_collection(settings.TOPIC_VALUES_COLLECTION)

db_business = client.get_database(settings.BUSINESS_DATABASE)
collection_business = db_business.get_collection(settings.BUSINESS_COLLECTION)


print('count', collection_business.count())


#################################################
# Geospatial query
#################################################

@app.route('/business_geo', methods=['GET'])
def get_business_geo_points():
	
	boundaries = json.loads(request.args.get('boundaries'))

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

@app.route('/review_batch', methods=['GET'])
def get_review_topic_batch():
	'''
	takes a list of businesses
	grabs their review ids
	then grabs the review's topic distribution
	return dictionary with {
	'0': [
			{'lat': lat, 'lon': lon, 'intensity': intensity},
			...
		],
	'1': [
			{'lat': lat, 'lon': lon, 'intensity': intensity},
			{'lat': lat, 'lon': lon, 'intensity': intensity},
			...
		], 
	}
	'''
	business_list = request.args.getlist('business_list[]')
	filter_value = request.args.get('filter_value')

	print('FILTER VALUE', filter_value)

	# get the review ids
	cursor = collection_reviews.find({'business': {'$in':business_list}})
	
	review_ids = [{'reviewId': x['reviewId'], 'location': x['location']} for x in list(cursor)]
	results = []

	
	for review in review_ids:
		# get all the topics for review
		topic_item = collection_topics.find_one({'reviewId': review['reviewId']})
		# print('topic item', topic_item)
		if topic_item:
			topic_exists = topic_item['topics'].get(filter_value)
			if topic_exists:
				topic_info = {
					'lat': review['location']['coordinates'][1],
					'lng': review['location']['coordinates'][0],
					'count': float(topic_exists)
				}
				results.append(topic_info)
		# print(review, ' finished')
					

	return jsonify(results)

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
	
	# get list of reviews for the business
	review_content_list = request.args.getlist('review_list[]')
	print('REIEW CONTENT LIST', type(review_content_list[0]))
	review_list = [eval(x)['reviewId'] for x in review_content_list]
	print('review content list',review_list)

	# get list of reviews for the business
	cursor = collection_topics.find({'reviewId': {'$in': review_list}})
	# print('TOPIC CURSOR', len([x for x in cursor]))

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
		print('REVIEW', review)
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
	print('avg',[sum(x[1])/len(x[1]) for x in sum_calcs.items()])
	# calculate average of each topic
	return jsonify([sum(x[1])/len(x[1]) for x in sum_calcs.items()])


API_KEY= settings.YELP_FUSION_API_KEY
API_HOST = 'https://api.yelp.com/v3/'
SEARCH_PATH = 'businesses/search'
BUSINESS_PATH = 'businesses/{id_value}' # .format(id_value=business_['id'])
REVIEWS_PATH = 'businesses/{id_value}/reviews' # .format(id_value=business_['id'])


DEFAULT_TERM = 'Longbridge Pizza'
DEFAULT_LOCATION = 'San Francisco'
SEARCH_LIMIT = 5

class RestaurantSearchForm(FlaskForm):
    """Contact form."""
    restaurant_name = StringField('Restaurant Name', [DataRequired()])
    restaurant_location = StringField('Restaurant Location', [DataRequired()])
    submit=SubmitField('Submit')


def api_request(host, path, api_key, url_params=None):
    """
    general api request function
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    print(url)
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

@app.route('/run_restaurant_search', methods=['GET'])
def run_restaurant_search():
	print(request.form['restaurant_name'])
	print(request.form['restaurant_location'])


@app.route('/business_details', methods=['GET'])
def search_business():

	term = request.args.get('restaurant_name')
	location = request.args.get('restaurant_location')

	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit':20
		   }
	business_result = api_request(API_HOST, SEARCH_PATH, API_KEY, url_params)['businesses']
	one_business = business_result[0]

	def bool_to_str(bool):
		if bool:
			return 'Yes'
		else:
			return 'No'

	def format_categories(categories_str):
		cat_list = [x['title'] for x in categories_str]
		if len(cat_list) <=1:
			return ' '.join(cat_list)
		else:
			return ', '.join(cat_list)
	
	def format_addresses(address_list):
		address_str = ''
		for add in address_list:
			if add != None:
				address_str += add
				address_str += ' '
		print(address_str)
		return address_str
			
	result = {
		'name': one_business['name'],
		'price': one_business['price'],
		'address': format_addresses([one_business['location']['address1'],
									one_business['location']['address2'],
									one_business['location']['city'],
									one_business['location']['country']]),
		'rating': one_business['rating'],
		'total_review_count': one_business['review_count'],
		'categories': format_categories(one_business['categories']),
		'phone': one_business['display_phone'],
		'is_closed': bool_to_str(one_business['is_closed']),
	}

	return jsonify(data=[{'field': x,'value': y} for x,y in result.items()])


def search_reviews(business_id):
	'''
	returns 3 reviews from each business
	'''

	review_path = REVIEW_PATH.format(id_value=business_id)

	return api_request(API_HOST, review_path, API_KEY)

def run_model(text):
	'''
	run the model on given text
	'''
	model_path = settings.model_path
	dictionary_path = settings.dictionary_path
	pp = Predict(model_path, dictionary_path)
	results = pp.run(text)
	return results 


@app.route('/')
def index():
	return render_template("index.html")        

@app.route("/search")
def search():

	return render_template("search.html")
	
	# if request.method == 'POST':
	# 	results = request.form
	# 	search_results = search_business(results['restaurant_name'], results['restaurant_location'])
	# 	print('search results', search_results)
	# 	return jsonify(result=search_results)
	# else:
	# 	form = RestaurantSearchForm()
	# 	if form.validate_on_submit():
	# 		return redicect(url_for('success'))
	# 	return render_template("search.html",form=form)

@app.route("/explore")
def explore():
	return render_template("explore.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/explore_topics")
def explore_topics():
	return render_template("explore_topics.html")

if __name__ == '__main__':
	app.run(debug=True)

