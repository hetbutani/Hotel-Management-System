from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from urllib.parse import unquote
import os
import traceback

app = Flask(__name__)
CORS(app)

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://hetbutani57:het5130O@cluster0.fqkimyy.mongodb.net/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['hotel_management_db']

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # This will catch everything sent to this function
    # We will manually route based on the path
    try:
        if 'rooms/featured' in path:
            rooms = list(db['rooms'].find({}, {'_id': 0}))
            return jsonify(rooms)
        elif 'rooms/search' in path:
            data = request.get_json()
            guests_str = data.get('guests', '1 Guest')
            guests = int(guests_str.split(' ')[0].replace('+', ''))
            query = {"capacity": {"$gte": guests}}
            available_rooms = list(db['rooms'].find(query, {'_id': 0}))
            return jsonify(available_rooms)
        elif 'rooms/details' in path:
            title = unquote(path.split('/')[-1])
            room = db['rooms'].find_one({"title": title}, {'_id': 0})
            return jsonify(room) if room else (jsonify({"error": f"Room '{title}' not found in database"}), 404)
        elif 'bookings' in path:
            data = request.get_json()
            db['bookings'].insert_one({
                "room_title": data.get('room_title'),
                "check_in": data.get('check_in'),
                "check_out": data.get('check_out'),
                "guests": data.get('guests'),
                "status": "Confirmed"
            })
            return jsonify({"message": "Booking successful"}), 201
        elif 'reviews' in path:
            reviews = list(db['reviews'].find({}, {'_id': 0}))
            return jsonify(reviews)
        elif 'health' in path:
            return jsonify({"status": "ok", "path_received": path})
        
        return jsonify({"error": "route not matched", "path": path}), 404
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run()
