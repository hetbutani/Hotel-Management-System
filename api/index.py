from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os
import razorpay
import traceback
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "luxe-stay-secret-key")
jwt = JWTManager(app)

# Razorpay Configuration
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_YourKeyId")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "YourKeySecret")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://hetbutani57:het5130O@cluster0.fqkimyy.mongodb.net/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['hotel_management_db']

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    try:
        # Auth Routes
        if 'auth/login' in path and request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            user = db['users'].find_one({"email": email})
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                access_token = create_access_token(identity={"email": email, "role": user['role']})
                return jsonify(access_token=access_token, role=user['role']), 200
            return jsonify({"message": "Invalid email or password"}), 401
            
        elif 'auth/signup' in path and request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'Guest')
            if db['users'].find_one({"email": email}):
                return jsonify({"message": "User already exists"}), 400
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db['users'].insert_one({"email": email, "password": hashed_password, "role": role})
            return jsonify({"message": "User created successfully"}), 201

        # Room Routes
        elif 'rooms/featured' in path:
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
            return jsonify(room) if room else (jsonify({"error": f"Room '{title}' not found"}), 404)

        # Booking Routes
        elif 'bookings' in path and request.method == 'POST':
            data = request.get_json()
            db['bookings'].insert_one({
                "room_title": data.get('room_title'),
                "check_in": data.get('check_in'),
                "check_out": data.get('check_out'),
                "guests": data.get('guests'),
                "customer_name": data.get('customer_name', 'Guest User'),
                "customer_email": data.get('customer_email', ''),
                "customer_phone": data.get('customer_phone', ''),
                "status": "Confirmed",
                "payment_id": data.get('payment_id'),
                "created_at": data.get('created_at')
            })
            return jsonify({"message": "Booking successful"}), 201

        # Review Routes
        elif 'reviews' in path:
            if request.method == 'POST':
                data = request.get_json()
                db['reviews'].insert_one({
                    "name": data.get('name'),
                    "role": data.get('role', 'Guest'),
                    "content": data.get('content'),
                    "rating": int(data.get('rating', 5)),
                    "avatar": f"https://i.pravatar.cc/150?u={data.get('name')}",
                    "created_at": data.get('created_at')
                })
                return jsonify({"message": "Review submitted successfully"}), 201
            else:
                reviews = list(db['reviews'].find({}, {'_id': 0}).sort('_id', -1))
                return jsonify(reviews)

        # Payment Routes
        elif 'payments/create_order' in path and request.method == 'POST':
            data = request.get_json()
            amount = int(data.get('amount')) * 100
            order = razorpay_client.order.create(data={"amount": amount, "currency": "INR", "payment_capture": 1})
            return jsonify(order), 200
            
        elif 'payments/verify' in path and request.method == 'POST':
            data = request.get_json()
            razorpay_client.utility.verify_payment_signature(data)
            return jsonify({"message": "Payment verified successfully"}), 200

        # Contact Route
        elif 'contact' in path and request.method == 'POST':
            data = request.get_json()
            db['contacts'].insert_one({
                "name": data.get('name'),
                "email": data.get('email'),
                "subject": data.get('subject'),
                "message": data.get('message'),
                "status": "New"
            })
            return jsonify({"message": "Message sent successfully"}), 201

        # Admin Stats Route
        elif 'admin/stats' in path:
            total_rooms = db['rooms'].count_documents({})
            total_bookings = db['bookings'].count_documents({})
            recent_bookings = list(db['bookings'].find({}, {'_id': 0}).sort('_id', -1).limit(5))
            
            # Simple revenue calculation (sum of prices of rooms in bookings)
            # This is a bit slow but fine for small datasets
            total_revenue = 0
            for b in db['bookings'].find({}):
                room = db['rooms'].find_one({"title": b.get('room_title')})
                if room:
                    total_revenue += room.get('price', 0)

            return jsonify({
                "total_rooms": total_rooms,
                "total_bookings": total_bookings,
                "total_revenue": total_revenue,
                "recent_bookings": recent_bookings
            })

        # All Bookings Route
        elif 'admin/bookings' in path:
            bookings = list(db['bookings'].find({}, {'_id': 0}).sort('_id', -1))
            return jsonify(bookings)

        # Staff Directory Route
        elif 'admin/staff' in path:
            # We'll fetch from a 'staff' collection. If it doesn't exist, we'll return sample data.
            staff_list = list(db['staff'].find({}, {'_id': 0}))
            if not staff_list:
                # Fallback sample data if collection is empty
                staff_list = [
                    {"staff_id": "STF001", "name": "John Doe", "room": "Ocean View Suite", "customer": "Sarah Miller"},
                    {"staff_id": "STF002", "name": "Jane Smith", "room": "Executive Room", "customer": "James Davis"},
                    {"staff_id": "STF003", "name": "Mike Ross", "room": "Penthouse Loft", "customer": "Emma Wilson"}
                ]
            return jsonify(staff_list)

        elif 'health' in path:
            return jsonify({"status": "ok", "path_received": path})
        
        return jsonify({"error": "route not matched", "path": path}), 404
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run()
