from flask import Flask, render_template, jsonify, request, redirect
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://tajunkim:wns41224--@cluster0.bxexa3c.mongodb.net/test')
dblaundry = client.dblaundry

from datetime import datetime, timedelta
from bson import ObjectId
import hashlib
import jwt
import uuid

SECRET_KEY = 'jungle'

@app.route('/')
def listPage():
    token_receive = request.cookies.get('mytoken')
    reservations = []
    week = ['월', '화', '수', '목', '금', '토', '일']
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = dblaundry.users.find_one({'id':payload['id']})
        for i in range(0, 7):
            reservation = list(dblaundry.reservations.find({'date':i}, {'_id':False}))
            reservations.append(reservation)
        return render_template('index.html', week = week, reservations = reservations, user_name = user_info['name'], user_id = user_info['userID'])
    except jwt.ExpiredSignatureError:
        return redirect('loginpage')
    except jwt.exceptions.DecodeError:
        return redirect('loginpage')

@app.route('/reservepage')
def reservePage():
    # time_receive = request.form['time_give']
    # id_receive = request.form['id_give']
    # name_receive = request.form['name_receive']
    time_receive = 9
    userId_receive = "1234"
    name_receive = "김태준"
    reservation = {'time': time_receive, 'userId':  userId_receive, 'name': name_receive}
    userId = "1234"

    return render_template('reserve.html', reservation=reservation, userId=userId)

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
            'exp':datetime.utcnow() + timedelta(hours=1)
        }
        print(payload)
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'아이디 또는 비밀번호가 일치하지 않습니다.'})

@app.route('/signuppage')
def signupPage():
    return render_template('signup.html')

# 예약하기 api
@app.route('/reserve', methods=["POST"])
def update_reservation():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    userId_receive = request.form['userId_give']
   
    dblaundry.reservations.find_one_and_update({'_id': ObjectId(id_receive)}, {'$set': {'name': name_receive, 'userId': userId_receive}})
    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})

# 예약취소 api
@app.route('/reserve/delete', methods=["POST"])
def delete_reservation():
    id_receive = request.form['id_give']
    dblaundry.reservations.find_one_and_update({'_id': ObjectId(id_receive)}, {'$set': {'name': '', 'userId': ''}})
    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})

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