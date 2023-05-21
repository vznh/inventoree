import csv
import json
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

@app.route('/confirm')
def display_confirmation():
    return render_template("confirm.html")

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
    for month in range(1, 13):
        # Create collection name using year and month name
        month_name = month_names[month]
        collection_name = f"{current_year}_{month_name}"
        collection = db[collection_name]

        # Create and insert documents for each type
        types = ["pants", "shirt", "dress", "outerwear", "accessories", "shoes"]
        for item_type in types:
            document = {
                "type": item_type,
                "quantity": 0,
                "student": 1,
                "date-time": []
            }
            # Append the current date-time to the date-time array
            document["date-time"].append(datetime.now().strftime("%d-%m-%y-%H"))

            # Insert the document into the collection
            collection.insert_one(document)

def check_out_item(collection, type_of_item: str, quantity_of_item: int, studentQ: bool, date: str, last_updated: int) -> int:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y-%H")
    collection.update_one({"type": f"{type_of_item}"}, 
                          {"$inc": {"quantity": -quantity_of_item}},
                          {"$push": {"date-time": formatted_datetime}})

# Increments item in database
def check_in_item(collection, type_of_item: str, quantity_of_item: int, studentQ: bool, date: str, last_updated: int) -> None:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y-%H")
    collection.update_one({"type": f"{type_of_item}"}, 
                          {"$inc": {"quantity": quantity_of_item}},
                          {"$push": {"date-time": formatted_datetime}} )

def import_data_from_ext(dataset):
    pass # To implement

def rename_collection(collection: str, new_name: str) -> None:
    db.collection.rename(new_name)
    

if __name__ == '__main__':
    app.run(debug=True)