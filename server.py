from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'friendsdb')

@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('index.html', all_friends = friends)

@app.route('/friends', methods=['POST'])
def create():
	query = "INSERT INTO friends(first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'occupation': request.form['occupation']
		}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/edit/<friend_id>', methods=['POST'])
def show(friend_id): #friend_id is the variable that you're passing
	query = "SELECT * FROM friends WHERE id = :specific_id" #this is the query you're sending to the database
	data = {'specific_id': friend_id} # this is the data you're sending to the datbase
	friends = mysql.query_db(query, data) #combine the query with the data and you'll get back data from the database
	return render_template('edit.html', friends=friends) #this sends you to the edit.html page with friends being the data you requested

@app.route('/delete/<friend_id>')
def delete(friend_id):
	query = "DELETE FROM friends WHERE id = :id" #this is the query
	data = {'id': friend_id} #this is the data
	mysql.query_db(query, data) #this is the result from the query with the data from the db
	return redirect('/') #redirect back to the front page

@app.route('/update/<friend_id>', methods=['POST'])
def update(friend_id):
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation, updated_at = NOW() WHERE id = :id" #the query that you're updating info from the db back to the db
	data = { #this is the data you'll be updating in the db
		'first_name': request.form['first_name'], 
		'last_name':  request.form['last_name'],
		'occupation': request.form['occupation'],
		'id': friend_id
		}
	mysql.query_db(query, data)
	return redirect('/')

app.run(debug=True)