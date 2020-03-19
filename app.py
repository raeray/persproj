from flask import Flask, render_template, url_for, request, redirect,jsonify
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
from flask_pymongo import MongoClient

# app.config["MONGO_URI"] = "mongodb://localhost:27017/Tags.Corpus"
# mongo = PyMongo(app)

client = MongoClient()
db_geo = client.get_database('geojson_flask')
collection_geo = db_geo.get_collection('COLLECTION_NAME')

@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    points = []
    iter_ = 0
    for item in collection_geo.find({'type': 'Point'}):
        points.append({
            "type": "Feature",
            "review_stars": item['review_stars'],
            "business_stars": item['business_stars'],
            "geometry": {
                "type": item['type'],
                "coordinates": [item['coordinates'][1],item['coordinates'][0]]
            }
        })
        iter_ += 1
        if iter_ > 10000:
            break
        # print(item)
    return jsonify(points)

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

