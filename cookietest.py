from flask import Flask,make_response,url_for,render_template,request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def limited_cookie():

    if request.method == 'POST':
        res = make_response("Setting limited cookie")
        expire_date = datetime.now() + timedelta(days=2)
        res.set_cookie('uname', "panda", expires=expire_date, secure=True, httponly=True)
        #print(res.delete_cookie('limited_cookie'))
        print(res)
        return res
    else:
        #uname = request.cookies.get('uname')
        #print(f"uname:{uname}")
        return render_template('login.html')

app.run(host="0.0.0.0",port=8080,debug=True)