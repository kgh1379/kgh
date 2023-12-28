import pymongo
from bson.objectid import ObjectId


# Create MongoDB client and connect to database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nuclear_medicine"]
receipts = db["receipts"]
dispatches = db["dispatches"]

# Create receipt and dispatch collections
def create_tables():
    receipts.create_index([("manufacturer", pymongo.ASCENDING)])
    dispatches.create_index([("receipt_id", pymongo.ASCENDING)])

# Insert receipt data
def insert_receipt(data):
    receipts.insert_one(data)

# Insert shipping data
def insert_dispatch(data):
    dispatches.insert_one({
        "receipt_id": ObjectId(data["receipt_id"]),
        "dispatch_date": data["dispatch_date"],
        "radiation_dose_rate": data["radiation_dose_rate_dispatch"],
        "checker": data["checker"]
    })

# Retrieve all receipt data
def get_receipts():
    return list(receipts.find())

# Search all shipment data
def get_dispatches():
    return list(dispatches.find())

# Search for undelivered generators by manufacturer
def get_unshipped_generators_by_manufacturer(manufacturer):
    dispatched_receipt_ids = [d["receipt_id"] for d in dispatches.find({}, {"receipt_id": 1})]
    return list(receipts.find({
        "manufacturer": manufacturer,
        "_id": {"$nin": dispatched_receipt_ids}
    }))

# Search for all undelivered generators
def get_unshipped_generators_all():
    dispatched_receipt_ids = [d["receipt_id"] for d in dispatches.find({}, {"receipt_id": 1})]
    return list(receipts.find({
        "_id": {"$nin": dispatched_receipt_ids}
    }))

# Search for available generators
def get_available_generators():
    dispatched_receipt_ids = [d["receipt_id"] for d in dispatches.find({}, {"receipt_id": 1})]
    return list(receipts.find({
        "_id": {"$nin": dispatched_receipt_ids}
    }, {"_id": 1}))

# Additional functions can be added here to fulfill the requirements of the RI&RP Section in gapp.py
