from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL

main = Flask(name)

main.config['MYSQL_HOST'] = 'davis-hackathon.cb3v6zq0wxva.us-west-1.rds.amazonaws.com'
main.config['MYSQL_USER'] = 'admin'
main.config['MYSQL_PASSWORD'] = 'password'
main.config['MYSQL_PORT'] = 3306
main.config['MYSQL_DB'] = 'davis-hackathon'

mysql = MySQL(main)

conn = mysql.connect()