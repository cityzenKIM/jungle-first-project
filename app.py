from pymongo import MongoClient
from flask import Flask, render_template, jsonify, Request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
dblaundry = client.dblaundry

# days = ['월','화','수','목','금','토','일']
# times = [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# for day in days:
#     for time in times:
#         dblaundry.dblaundry.insert_one({'time':'time','요일':'day','이용자':'','예약자id':''})

@app.route('/')
def listPage():
    # laundrydata = list(dblaundry.week.find({},{'_id':0}))
    # laundrydata_07 = list(dblaundry.week.find({'요일':'월'},{'_id':0}))
    laundrydata_mon = list(dblaundry.week.find({},{'_id':0}))
    laundrydata_tue = list(dblaundry.week.find({'date':'화'},{'_id':0}))
    laundrydata_wed = list(dblaundry.week.find({'date':'수'},{'_id':0}))
    laundrydata_thu = list(dblaundry.week.find({'date':'목'},{'_id':0}))
    laundrydata_fri = list(dblaundry.week.find({'date':'금'},{'_id':0}))
    laundrydata_sat = list(dblaundry.week.find({'date':'토'},{'_id':0}))
    laundrydata_sun = list(dblaundry.week.find({'date':'일'},{'_id':0}))
    
    laundrydata_sum = []
    laundrydata_sum.append(laundrydata_mon)
    laundrydata_sum.append(laundrydata_tue)
    laundrydata_sum.append(laundrydata_wed)
    laundrydata_sum.append(laundrydata_thu)
    laundrydata_sum.append(laundrydata_fri)
    laundrydata_sum.append(laundrydata_sat)
    laundrydata_sum.append(laundrydata_sun)
    return render_template('index.html', laundryDatas_sum = laundrydata_mon)

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