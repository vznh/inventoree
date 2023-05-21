import csv
import json
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL
import time

app = Flask(__name__)

# SQL Connection
app.config['MYSQL_HOST'] = 'Jasons-MacBook-Pro-3.local'
app.config['MYSQL_USER'] = 'root@localhost'
app.config['MYSQL_PASSWORD'] = 'WheelyStrongPwd'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)

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

@app.route('/removeInventory')
def display_editor():
    return render_template("removeInventory.html")


'''
To be called functions
'''
def recieveFields():
    pass
def check_out(item: int) -> int:
    try: # Implement taking out of SQL based on what ID is correlated
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "DELETE FROM curr_stock WHERE id = %s"
        cursor.execute(query, (item,))
        conn.commit()
        
        cursor.close()
        conn.close()
    except Exception: # If it doesn't exist, return error code
        cursor.close()
        conn.close()
        return 201
    else: # If it works, return good code
        return 200


def check_in(type_of_item: str, quantity_of_item: int, day_of_checkin: str, time_of_checkin: int) -> None:
    '''
    Added pseudocode:
    Initialize MySQL cursor + database
    When something is added to database, add:
        - A randomized ID
        - Type
        - Quantity
        - Day
    
    if successful, return int 200
    '''
    # Establish SQL connection + parameters
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO your_table_name (type, quantity, day, id) VALUES (%s, %s, %s, %s)"
        val = (type_of_item, quantity_of_item, day_of_checkin, time_of_checkin)
        cursor.execute(query, val)
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(str(e))
        return print(201)
    else:
        return print(200)

if __name__ == '__main__':
    check_in("pants", 2, "05/20/23", 15)
    app.run(debug=True)