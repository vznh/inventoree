from flask import Flask, request
from flaskext.mysql import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'inventoree-database.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'inventoreeadmin'
app.config['MYSQL_PASSWORD'] = 'HackDavis2023'
app.config['MYSQL_DB'] = 'inventoree-database'
mysql = MySQL(app)
def submit():
    # Access the submitted data
    data = request.form['data']
    
    # Perform any necessary data processing/validation
    # ...
    
    # Store the data in the database
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tablename (columnname) VALUES (%s)", (data,))
    conn.commit()
    conn.close()
    
    # Return a response to the client
    return 'Data stored successfully!'