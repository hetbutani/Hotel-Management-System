from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os
import razorpay

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Razorpay Configuration (Replace with your actual keys)
RAZORPAY_KEY_ID = "rzp_test_YourKeyId"
RAZORPAY_KEY_SECRET = "YourKeySecret"
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "luxe-stay-secret-key" # Change this in production
jwt = JWTManager(app)

MONGO_URI = "mongodb+srv://hetbutani57:het5130O@cluster0.fqkimyy.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['hotel_management_db']
rooms_collection = db['rooms']
users_collection = db['users']
reviews_collection = db['reviews']
bookings_collection = db['bookings']
contacts_collection = db['contacts']

# --- Routes: Auth ---

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'Guest')

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "role": role
    })
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity={"email": email, "role": user['role']})
        return jsonify(access_token=access_token, role=user['role']), 200

    return jsonify({"message": "Invalid email or password"}), 401

# --- Routes: Rooms ---

@app.route('/api/rooms/featured', methods=['GET'])
def get_featured_rooms():
    try:
        rooms = list(rooms_collection.find({}, {'_id': 0}))
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rooms/search', methods=['POST'])
def search_rooms():
    try:
        data = request.get_json()
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        guests_str = data.get('guests', '1 Guest')
        
        # Extract number from "2 Guests" string
        guests = int(guests_str.split(' ')[0].replace('+', ''))
        
        # Simple filter by capacity for now
        # In a real app, we would join with bookings to check availability for dates
        query = {"capacity": {"$gte": guests}}
        available_rooms = list(rooms_collection.find(query, {'_id': 0}))
        
        return jsonify(available_rooms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rooms/details/<title>', methods=['GET'])
def get_room_details(title):
    try:
        room = rooms_collection.find_one({"title": title}, {'_id': 0})
        if room:
            return jsonify(room), 200
        return jsonify({"message": "Room not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Routes: Bookings ---

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        booking = {
            "room_title": data.get('room_title'),
            "check_in": data.get('check_in'),
            "check_out": data.get('check_out'),
            "guests": data.get('guests'),
            "customer_name": data.get('customer_name', 'Guest User'),
            "status": "Confirmed"
        }
        bookings_collection.insert_one(booking)
        return jsonify({"message": "Booking successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Routes: Payments ---

@app.route('/api/payments/create_order', methods=['POST'])
def create_payment_order():
    try:
        data = request.get_json()
        amount = int(data.get('amount')) * 100 # Convert to paise
        
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1 # Auto capture
        }
        
        order = razorpay_client.order.create(data=order_data)
        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payments/verify', methods=['POST'])
def verify_payment():
    try:
        data = request.get_json()
        params_dict = {
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        }
        
        # Verify signature
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Update booking status if needed
        # (Usually we would pass the booking_id in the order creation and store it)
        
        return jsonify({"message": "Payment verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Payment verification failed"}), 400

# --- Routes: Contact ---

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        message = {
            "name": data.get('name'),
            "email": data.get('email'),
            "subject": data.get('subject'),
            "message": data.get('message'),
            "status": "New"
        }
        contacts_collection.insert_one(message)
        return jsonify({"message": "Message sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Routes: Reviews ---

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    try:
        reviews = list(reviews_collection.find({}, {'_id': 0}))
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use 5005 to avoid conflicts
    app.run(debug=True, host='0.0.0.0', port=5005)
