from pymongo import MongoClient
from flask import Flask, render_template, jsonify, Request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dblaundry

@app.route('/')
def listPage():
    return render_template('index.html')

@app.route('/reservepage')
def reservePage():
    return render_template('reserve.html')

@app.route('/loginpage')
def loginPage():
    return render_template('login.html')

@app.route('/signuppage')
def signupPage():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)