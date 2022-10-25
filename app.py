from flask import Flask, render_template, jsonify, request, redirect
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://tajunkim:wns41224--@cluster0.bxexa3c.mongodb.net/test')
dblaundry = client.dblaundry

from datetime import datetime, timedelta
import hashlib
import jwt
import uuid

SECRET_KEY = 'jungle'

@app.route('/')
def listPage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = dblaundry.users.find_one({'id':payload['id']})
        
        return render_template('index.html', user_name = user_info['name'], user_id = user_info['userID'])
    except jwt.ExpiredSignatureError:
        return redirect('loginpage')
    except jwt.exceptions.DecodeError:
        return redirect('loginpage')

@app.route('/reservepage')
def reservePage():
    return render_template('reserve.html')

@app.route('/loginpage')
def loginPage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = dblaundry.users.find_one({'id':payload['id']})
        return redirect('/')
    except jwt.ExpiredSignatureError:
        return render_template('login.html')
    except jwt.exceptions.DecodeError:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give'] 
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = dblaundry.users.find_one({'id':id_receive, 'pw':pw_hash}, {'_id':False})

    if result is not None:
        payload = {
            'id':id_receive,
            'exp':datetime.utcnow() + timedelta(seconds=10)
        }
        print(payload)
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'아이디 또는 비밀번호가 일치하지 않습니다.'})

@app.route('/signuppage')
def signupPage():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    jgclass_receive = request.form['jungle_class_give']
    gender_receive = request.form['gender_give']
    if name_receive == '' or id_receive == '' or pw_receive == '':
        return jsonify({'result':'success', 'msg':'None'})
    if dblaundry.users.find_one({'name':name_receive}) is not None:
        return jsonify({'result':'success', 'msg':'nameoverlap'})
    else:
        userID = str(uuid.uuid4())
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        dblaundry.users.insert_one({
            'name':name_receive,
            'id':id_receive,
            'pw':pw_hash,
            'class':jgclass_receive,
            'gender':gender_receive,
            'userID':userID
        })
        return jsonify({'result':'success', 'msg':'signup'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)