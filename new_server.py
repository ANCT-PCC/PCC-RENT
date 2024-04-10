from flask import Flask,redirect, url_for, render_template, request, session

from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'waitforme'
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug = True,port=5000,)