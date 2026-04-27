from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os
import razorpay
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "luxe-stay-secret-key")
jwt = JWTManager(app)

# Razorpay Configuration
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_YourKeyId")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "YourKeySecret")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# MongoDB Connection with Timeout
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://hetbutani57:het5130O@cluster0.fqkimyy.mongodb.net/")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['hotel_management_db']
    # Trigger a connection check
    client.admin.command('ping')
    print("MongoDB Connected Successfully")
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

# Helper for collections (to avoid early crash)
def get_coll(name):
    return db[name]

# --- Routes ---

@app.route('/api/health')
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "database": "connected" if db else "failed"}), 200

@app.route('/api/rooms/featured')
@app.route('/rooms/featured')
def get_featured_rooms():
    try:
        rooms = list(get_coll('rooms').find({}, {'_id': 0}))
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/api/rooms/details/<title>')
@app.route('/rooms/details/<title>')
def get_room_details(title):
    try:
        room = get_coll('rooms').find_one({"title": title}, {'_id': 0})
        if room:
            return jsonify(room), 200
        return jsonify({"error": f"Room '{title}' not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/api/reviews')
@app.route('/reviews')
def get_reviews():
    try:
        reviews = list(get_coll('reviews').find({}, {'_id': 0}))
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

# Add other routes similarly...
@app.route('/api/bookings', methods=['POST'])
@app.route('/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        get_coll('bookings').insert_one({
            "room_title": data.get('room_title'),
            "check_in": data.get('check_in'),
            "check_out": data.get('check_out'),
            "guests": data.get('guests'),
            "payment_id": data.get('payment_id'),
            "status": "Confirmed"
        })
        return jsonify({"message": "Booking successful"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/contact', methods=['POST'])
@app.route('/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        get_coll('contacts').insert_one({
            "name": data.get('name'),
            "email": data.get('email'),
            "subject": data.get('subject'),
            "message": data.get('message')
        })
        return jsonify({"message": "Sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payments/create_order', methods=['POST'])
@app.route('/payments/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        order = razorpay_client.order.create(data={"amount": int(data['amount'])*100, "currency": "INR", "payment_capture": 1})
        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payments/verify', methods=['POST'])
@app.route('/payments/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        razorpay_client.utility.verify_payment_signature(data)
        return jsonify({"status": "verified"}), 200
    except:
        return jsonify({"status": "failed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
