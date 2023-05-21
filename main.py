from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

load_dotenv()

# Database connection
client = MongoClient(os.getenv('uri'))
db = client["db"]

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def page_analytics():
    return render_template('analytics.html')

@app.route('/addInventory')
def display_options():
    return render_template("addInventory.html")

@app.route('/manualEntry')
def display_fields():
    return render_template("pass.html")

@app.route('/editInventory')
def display_editor():
    return render_template("editInventory.html")

@app.route('/processing')
def display_confirmation():
    return render_template("processing.html")

'''
To be called functions
'''

def initialize_database():
    month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
    }
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month
    # Initialize collections for each month
    collections = db.list_collection_names()
    # Count the number of collections
    collection_count = len(collections)
    if collection_count == 0:
        for month in range(1, 13):
            # Create collection name using year and month name
            month_name = month_names[month]
            collection_name = f"{current_year}_{month_name}"
            collection = db[collection_name]

            # Create and insert documents for each type
            types = ["pants", "shirts", "dress", "outerwear", "accessories", "shoes", "books", "household", "school supplies", "bottoms", "misc."]
            for item_type in types:
                document = {
                    "type": item_type,
                    "quantity": 0,
                    "student": [],
                    "date-time": []
                }
                # Append the current date-time to the date-time array
                document["date-time"].append(datetime.now().strftime("%d-%m-%y-%H"))

                # Insert the document into the collection
                collection.insert_one(document)

# Decrements and logs check-out
def check_out_item(collection_name: str, type_of_item: str, quantity_of_item: int) -> int:
    collection = db[collection_name]
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y-%H") + ", check-out"
    collection.update_one(
        {"type": type_of_item},
        {
            "$inc": {"quantity": -quantity_of_item},
            "$push": {"date-time": formatted_datetime}
        },
        upsert=False
    )

# Increments item in database
def check_in_item(collection_name: str, type_of_item: str, quantity_of_item: int, studentQ: bool) -> None:
    collection = db[collection_name]
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y-%H") + ", check-in"
    collection.update_one(
        {"type": type_of_item},
        {
            "$inc": {"quantity": quantity_of_item},
            "$push": {
                "student": studentQ,
                "date-time": formatted_datetime
            }
        },
        upsert=False  # Set upsert to False
    )

def import_data_from_ext(dataset):
    pass # To implement

def rename_collection(collection: str, new_name: str) -> None: # Future implementation
    db.collection.rename(new_name)

def emergency_drop(): # Use in conjunction with initialize_database()
    # Get a list of all collections
    collections = db.list_collection_names()

    # Remove each collection
    for collection_name in collections:
        db[collection_name].drop()

def find_to_return(collection_name) -> dict:
    data_map = dict()
    base = db[collection_name]
    documents = base.find()
    for document in documents:
        item_type = document["type"]
        quantity = document["quantity"]
        student = document["student"]
        date_times = document["date-time"]
        
        # Store the extracted data in the dictionary
        data_map[item_type] = {
            "quantity": quantity,
            "student": student,
            "date_times": date_times
    }
    return data_map
    
if __name__ == '__main__':
    app.run(debug=True)