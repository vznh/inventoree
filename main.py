import csv
import json
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

# SQL Connection
client = MongoClient(os.getenv('uri'))
db = client["db"]
collection = db["collection"]


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


'''
To be called functions
'''
def recieveFields():
    pass
def check_out(item: int) -> int:
    pass


def check_in(type_of_item: str, quantity_of_item: int, day_of_checkin: str, time_of_checkin: int) -> None:
   pass
    

if __name__ == '__main__':
    check_in("pants", 2, "05/20/23", 15)
    app.run(debug=True)