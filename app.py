from flask import Flask, render_template, url_for, request, redirect,jsonify
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

client = MongoClient()
settings = Settings()
db_geo = client.get_database(settings.GEO_DATABASE)
collection_geo = db_geo.get_collection(settings.GEO_COLLECTION)

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
    return render_template("index.html")        

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

if __name__ == '__main__':
    app.run(debug=True)

