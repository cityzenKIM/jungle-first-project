from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)

# import certifi
# ca=certifi.where()
# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://tajunkim:wns41224--@cluster0.bxexa3c.mongodb.net/test', tlsCAFile=ca)
from pymongo import MongoClient
client = MongoClient('mongodb://ajm0718:qhemzk0204@15.165.248.49', 27017)
dblaundry = client.dblaundry

import datetime
import hashlib
import jwt
import uuid
import re

SECRET_KEY = 'jungle'

@app.route('/')
def listPage():
    token_receive = request.cookies.get('mytoken')
    reservations = []
    week = ['월', '화', '수', '목', '금', '토', '일']
    thisWeekDay = datetime.datetime.today().weekday()
    weekDay = dblaundry.thisweekday.find_one({'week':'day'}, {'_id':False})
    if thisWeekDay != weekDay['weekday']:
        dblaundry.reservations.update_many({'date':weekDay['weekday']}, {'$set':{'name':False, 'userID':False}})
        dblaundry.thisweekday.update_one({'week':'day'}, {'$set':{'weekday':thisWeekDay}})
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = dblaundry.users.find_one({'id':payload['id']})
        if user_info['class'] == 'red':
            for i in range(0, 7):
                reservation = list(dblaundry.reservations.find({'date':i, 'class':'red'}, {'_id':False}))
                reservations.append(reservation)
            return render_template('index.html', toDay = weekDay, week = week, reservations = reservations, user_name = user_info['name'], user_id = user_info['userID'])
        elif user_info['class'] == 'blue':
            for i in range(0, 7):
                reservation = list(dblaundry.reservations.find({'date':i, 'class':'blue'}, {'_id':False}))
                reservations.append(reservation)
            return render_template('index.html', toDay = weekDay, week = week, reservations = reservations, user_name = user_info['name'], user_id = user_info['userID'])
    except jwt.ExpiredSignatureError:
        return redirect('loginpage')
    except jwt.exceptions.DecodeError:
        return redirect('loginpage')


@app.route('/loginpage')
def loginPage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']).decode('utf8')
        # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
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
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf8')
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
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
    reservation = dblaundry.reservations.find_one({'timeID': id_receive})
    if reservation['name'] == False:
        dblaundry.reservations.find_one_and_update({'timeID': id_receive}, {'$set': {'name': name_receive, 'userID': userId_receive}})
        return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})
    else:
        return jsonify({'result': 'fail', 'msg': '이미 예약된 시간입니다.'})

# 예약취소 api
@app.route('/reserve/delete', methods=["POST"])
def delete_reservation():
    id_receive = request.form['id_give']
    dblaundry.reservations.find_one_and_update({'timeID': id_receive}, {'$set': {'name': False, 'userID': False}})
    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})

@app.route('/signup', methods=['POST'])
def signup():
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    jgclass_receive = request.form['jungle_class_give']
    gender_receive = request.form['gender_give']
    if name_receive == '' or id_receive == '' or pw_receive == '':
        return jsonify({'result':'None', 'msg':'모두 입력해주세요'})
    elif re.search(r'[a-zA-Z가-힣]{2,10}$', name_receive) is None:
        return jsonify({'result':'nameerr', 'msg':'이름은 숫자, 특수문자 제외 2~10자까지만 사용가능합니다.'})
    elif re.search(r'[A-Za-z0-9!@#$%^&*]{4,10}$', id_receive) is None:
        return jsonify({'result':'iderr', 'msg':'아이디는 한글 제외 4~10자까지만 사용가능합니다.'})
    elif re.search(r'[a-zA-Z0-9!@#$%^&*]{4,20}$', pw_receive) is None:
        return jsonify({'result':'pwerr', 'msg':'패스워드는 한글 제외 4~20자까지만 사용가능합니다.'})
    elif dblaundry.users.find_one({'name':name_receive}) is not None:
        return jsonify({'result':'nameoverlap', 'msg':'이름이 중복됩니다.'})
    elif dblaundry.users.find_one({'id':id_receive}) is not None:
        return jsonify({'result':'idoverlap', 'msg':'아이디가 중복됩니다.'})
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
    app.run('0.0.0.0', port=5000)