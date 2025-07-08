from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.github_events
events = db.events

def save_event(data):
    events.insert_one(data)

def get_latest_events():
    return list(events.find().sort("_id", -1).limit(10))
