import dbc
from flask import Flask , request
app = Flask(__name__, static_folder='.', static_url_path='')

CSV_FILE_NAME = "sales_data.csv"
print("サーバー開始")

@app.route('/')
def index():
    return app.send_static_file('test.html')

app.run(port=8000)
