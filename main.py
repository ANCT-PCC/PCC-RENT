from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, session,flash
import json , dbc

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'secret_key'
app.config['USERNAME'] = 'user'
app.config['PASSWORD'] = 'pass'


CORS(app)


@app.after_request
def after_request(response):
    allowed_origins = ['http://127.0.0.1:443/', 'http://127.0.0.1:8080/']
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/')
def index():
    if "flag" in session and session["flag"]:
        return render_template('dashboard.html', username=session["username"])
    return redirect('/login')

@app.route('/login',methods=['GET'])
def login():
    if "flag" in session and session["flag"]:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_job():

    res = request.json
    data = json.loads(json.dumps(res))[0]
    username = data['uname']
    password = data['passwd']
    print(username)
    print(password)

    session["flag"] = False
    if username != app.config['USERNAME']:
        flash('ユーザ名が異なります')
    elif password != app.config['PASSWORD']:
        flash('パスワードが異なります')
    else:
        session["flag"] = True
        session["username"] = username
    if session["flag"]:
        print("DEBUG 1")
        return render_template('dashboard.html', username=session["username"])
    elif session["flag"] == False:
        print("DEBUG 2")
        return redirect('/login'),4545
    
    print("DEBUG 3")

app.run(port=443,host="0.0.0.0",debug=True)