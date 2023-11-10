import dbc ,json
from flask import Flask , request
app = Flask(__name__, static_folder='.', static_url_path='')

CSV_FILE_NAME = "sales_data.csv"
print("サーバー開始")

@app.route('/')
def index():
    return app.send_static_file('test.html')

@app.route('/test')
def test():
    print("----------")
    for i in range(4):
        dbc.create_new_user(f"test{i}",f"{i}@",1,"NO")
        dbc.create_new_item(f"item{i}",i,"NO",1,"NO","none")

    print("----------")

    print("ユーザー一覧")

app.run(port=8000)
