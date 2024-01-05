import dbc ,json
from flask import Flask , request
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')

CORS(app)

print("サーバー開始")

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
    return app.send_static_file('login/login.html')

@app.route('/login_phase',methods=['POST'])
def login_job():
    print("DEBUG Python 1")
    res = request.json
    print(json.loads(json.dumps(res))[0]['passwd'])
    return "OK"

app.run(port=443,host="0.0.0.0",debug=True)
