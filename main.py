import dbc ,json
from flask import Flask , request
app = Flask(__name__, static_folder='.', static_url_path='')

print("サーバー開始")

@app.route('/')
def index():
    return app.send_static_file('main.html')

app.run(port=8000,host="0.0.0.0")
