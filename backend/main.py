from / import app.py #Work in sync with app.py that Jason is working on
import csv
import json
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL
app = Flask(__name__)

#All the login info for Microsoft Azure MySQL Database
app.config['MYSQL_HOST'] = 'inventoree-database.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'inventoreeadmin'
app.config['MYSQL_PASSWORD'] = 'HackDavis2023'
app.config['MYSQL_DB'] = 'inventoree-database'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("base.html")

@app.route('/analytics')
def load_analytics():
    return render_template("analytics.html")


@app.route('/clothing', methods=['POST'])
def add_clothing():
    '''
    Take the json or csv file from the frontend, extract the data and store in SQL database
    '''
    #establish SQL connection and create all the parameters
    conn = mysql.connection()
    cursor = conn.cursor()
    query = "INSERT INTO clothing (type, size, color, donor) VALUES (%s, %s, %s, %s)"
    # Check if file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']

    # Check if the file is a JSON or CSV file
    if file.filename.endswith('.json'):
        try:
            data = file.read().decode('utf-8')
            clothing_items = json.loads(data)
            for item in clothing_items:
                clothing_type = item['type']
                size = item['size']
                color = item['color']
                donor = item['donor']
                
                # Store the data in the database
                values = (clothing_type, size, color, donor)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
            
            return jsonify({'message': 'Clothing items added successfully!'})
        except Exception as e:
            return jsonify({'error': 'Error processing JSON file'})

    elif file.filename.endswith('.csv'):
        try:
            clothing_items = csv.DictReader(file)
            for item in clothing_items:
                clothing_type = item['type']
                size = item['size']
                color = item['color']
                donor = item['donor']
                
                # Store the data in the database
                values = (clothing_type, size, color, donor)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
            
            return jsonify({'message': 'Clothing items added successfully!'})
        except Exception as e:
            return jsonify({'error': 'Error processing CSV file'})

    else:
        return jsonify({'error': 'Invalid file format'})


if __name__ == '__main__':
    app.run(debug=True)