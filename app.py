
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from bson import ObjectId
app = Flask(__name__)

client = MongoClient('mongodb+srv://tajunkim:wns41224--@cluster0.bxexa3c.mongodb.net/test')
dblaundry = client.dblaundry

@app.route('/')
def listPage():
    return render_template('index.html')

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
    return render_template('login.html')

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)