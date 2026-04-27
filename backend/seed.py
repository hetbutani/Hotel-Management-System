from pymongo import MongoClient
import bcrypt

MONGO_URI = "mongodb+srv://hetbutani57:het5130O@cluster0.fqkimyy.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['hotel_management_db']

rooms_collection = db['rooms']
users_collection = db['users']
reviews_collection = db['reviews']

# --- Seed Rooms ---
featured_rooms = [
    {
        "title": "Ocean View Suite",
        "price": 450,
        "rating": 4.9,
        "capacity": 2,
        "description": "Spacious 60sqm suite featuring panoramic ocean views, a private balcony, and premium amenities.",
        "features": [{"icon": "king_bed", "text": "King Bed"}, {"icon": "wifi", "text": "Free Wifi"}, {"icon": "balcony", "text": "Balcony"}],
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCYSQnhB7W2qNHuXyYDsbDqX7OAdfPvkPZin_KGnYZIdT6fl7AoniJdohFYMJWddbkLJpkQa2QQS0usWgQQ3un2Nu2vukAV3Lkf4h12bkDFSKKPa38uSM01OwwyZQhFKIOawoz6NwsDbY0PwftOvDxrVPGE-MiT5sPrzrxksndWtaaI_qt-gwcKMvx1x-6sTO3jX5PoMl4Vpv-5p7lkRXXFea_fJ_5nhXvvvFuDKpDFdRRMiHOw_z_UDUqt2ASQOb31SVtHQu8vz8aU"
    },
    {
        "title": "Executive Room",
        "price": 320,
        "rating": 4.8,
        "capacity": 2,
        "description": "Designed for the modern traveler, offering a dedicated workspace and access to the Executive Lounge.",
        "features": [{"icon": "king_bed", "text": "King Bed"}, {"icon": "desk", "text": "Workspace"}, {"icon": "local_cafe", "text": "Lounge Access"}],
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDRw3Srg7TCr8D72_Urp3l_EG97iV2ioFs7bXamnZrEQ58YdOvJ48oyuKi8GeApCWp0MJZAeETbVU2l5Rs3wQ8T9nmo8bOfY53BVTN35jLVsdjwoMSc1MnBh2UizV_8VHDFMqE4Zx1h1djd-QV8uGTlz3x6xXCDQARmBhHGNt5vbquyoHkN0tMhSNv0XKe9vR0SovEYCzPRGEvBElX1YYOamKSQsV6RB4_1jqZDgZDFV3fTrditc7UF7lsSn_osC4m4sPh-fZ3oUc5t"
    },
    {
        "title": "Penthouse Loft",
        "price": 850,
        "rating": 5.0,
        "capacity": 4,
        "description": "The ultimate luxury experience. A two-story loft with a private terrace and plunge pool.",
        "features": [{"icon": "king_bed", "text": "2 King Beds"}, {"icon": "pool", "text": "Private Pool"}, {"icon": "room_service", "text": "Butler Service"}],
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuAfcEnrGLSDl_Wv3nUmcwwF346FPrMCziepQE6_XR5qksdYLMibWLhf1jcDKioBdetAK9zA6eruJffelha7MfhhLKNALCWZuI3-Uxw9u7797RgzPDEkBRUqzXJQaa_x3T4ehbWwMTed5tCMEZEC225yNxNdphlFwV9_bxpUk5NWfPmFonJB2C8x6hBB7H3mMhjrr66WNvIaqdBRskUcVdbgKEGXutBe3G87jdOOXYfpJH-fjJxZnGHFtZiGkV8_cgJtNO3XGfpCLzEZ"
    }
]

# --- Seed Reviews ---
sample_reviews = [
    {
        "name": "James Miller",
        "role": "Business Traveler",
        "content": "The attention to detail and service at LuxeStay is simply unmatched. The Executive Room was perfect for my stay.",
        "rating": 5,
        "avatar": "https://i.pravatar.cc/150?u=james"
    },
    {
        "name": "Elena Rodriguez",
        "role": "Leisure Guest",
        "content": "Waking up to the ocean view from our suite was a dream. Every moment felt like pure luxury.",
        "rating": 5,
        "avatar": "https://i.pravatar.cc/150?u=elena"
    },
    {
        "name": "Marcus Chen",
        "role": "Frequent Guest",
        "content": "LuxeStay has become my home away from home. The staff is professional and the facilities are world-class.",
        "rating": 4,
        "avatar": "https://i.pravatar.cc/150?u=marcus"
    }
]

# --- Seed Admin User ---
admin_email = "admin@luxestay.com"
admin_password = "admin123"
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

print("Clearing collections...")
rooms_collection.delete_many({})
users_collection.delete_many({})
reviews_collection.delete_many({})

print("Seeding Rooms...")
rooms_collection.insert_many(featured_rooms)

print("Seeding Reviews...")
reviews_collection.insert_many(sample_reviews)

print("Seeding Admin User...")
users_collection.insert_one({
    "email": admin_email,
    "password": hashed_password,
    "role": "Admin"
})

print("Successfully seeded the database!")
