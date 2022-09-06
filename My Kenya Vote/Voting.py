
from sqlite3 import Cursor
from flask import*

import pymysql
 
app = Flask(__name__)

app.secret_key = '12WEhr&88?8J*&9_'



# ID card login

@app.route('/idlogin', methods=['POST','GET'])
def login():

    if request.method == 'POST':
        connection = pymysql.connect(host='localhost', user='root', password='', database='voting')

        id_number = request.form['id_number']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        district_of_birth = request.form['district_of_birth']
        place_of_issue = request.form['place_of_issue']
        date_of_issue = request.form['date_of_issue']

        cursor = connection.cursor()
        sql = 'SELECT * FROM iddetails WHERE id_number=%s AND date_of_birth=%s AND gender=%s AND district_of_birth=%s AND place_of_issue=%s AND date_of_issue=%s'
        cursor.execute(sql, (id_number , date_of_birth , gender , district_of_birth , place_of_issue , date_of_issue))

        if cursor.rowcount == 0:
            return render_template('idlogin.html', msg='ERROR, Your National ID details does not match')
        elif cursor.rowcount == 1:
            session['key'] = id_number
            return render_template('vclogin.html', msg='Login Successfuly')
        else:
            return render_template('idlogin.html', msg='Something is wrong')
    else:
        return render_template('idlogin.html')


# Voters card login

@app.route('/vclogin', methods=['POST','GET'])
def vclogin():

    if request.method == 'POST':
        connection = pymysql.connect(host='localhost', user='root', password='', database='voting')

        electors_no = request.form['electors_no']
        full_name = request.form['full_name']
        id_number = request.form['id_number']
        constituency = request.form['constituency']
       

        cursor = connection.cursor()
        sql = 'SELECT * FROM vcdetails WHERE electors_no=%s AND full_name=%s AND id_number=%s AND constituency=%s'
        cursor.execute(sql, (electors_no , full_name , id_number , constituency ))

        if cursor.rowcount == 0:
            return render_template('vclogin.html', msg='ERROR, Your Voters Card details does not match')
        elif cursor.rowcount == 1:
            return render_template('homepage.html', msg='Login Successfuly')
        else:
            return render_template('vclogin.html', msg='Something is wrong')
    else:
        return render_template('vclogin.html')

@app.route('/candidates')
def candidates():

    return render_template('candidates.html')

@app.route('/president', methods=['POST', 'GET'])
def president():

    if request.method == 'POST':
        connection = pymysql.connect(host='localhost', user='root', password='', database='voting')
        president = request.form['president']

        
        cursor = connection.cursor()
        sql = 'SELECT * FROM presidents WHERE id=%s'
        cursor.execute (sql,(president))
        row= cursor.fetchone()
        votes = row[3]
        updated_votes  = votes + 1

        sql1 = 'UPDATE presidents SET votes = %s where id = %s'
        cursor1 = connection.cursor()
        cursor1.execute (sql1,(updated_votes, president))
        connection.commit()
        return redirect('/results')
    else:    
        return render_template('president.html')


@app.route('/results')
def passengers():
    connection = pymysql.connect(host='localhost' , user='root', password='', database='voting')

    cursor = connection.cursor()
    sql = 'SELECT*FROM presidents'
    cursor.execute(sql)

    data = cursor.fetchall()

    return render_template('results.html', rows = data)


@app.route('/end')
def end():

    return render_template('thankyou.html')


@app.route('/signout')
def signout():
    session.pop('key', None)
    return redirect('/end')   # take user to home route after logout

    


app.run(debug=True)