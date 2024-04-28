from flask import Flask, redirect, url_for, render_template, request,make_response
from datetime import timedelta #時間情報を用いるため
from datetime import datetime
import dbc

app = Flask(__name__)

app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=5) # -> 5分 #(days=5) -> 5日保存

#ログイン時にトークンを発行
def setlogininfo(uid:str,passwd:str):

    passwd_flag = True

    if passwd_flag == True:
        content = 'abcdefg0123' #一意のトークン
        response = make_response(content)
        max_age = 60*60 #1時間
        expires = int(datetime.now().timestamp())+max_age
        response.set_cookie('token',value=uid,max_age=max_age,path='/',secure=None,httponly=False)

        return response #ログインが正常であれば、トークンを発行
    else:
        return None

#トークンの有効・無効を確認する
def checkToken(token:str):
    #DBを参照してくる。
    #dbc.search_userinfo_from_name(uname)

    #Trueの場合、usernameは任意の名前
    #Falseの場合、usernameはNone
    username = "None"

    return False , username

@app.route('/',methods=['GET'])
def index():
    token = request.cookies.get('token',None)
    #token = 'abcd1234'
    ckFlag,uname = checkToken(token=token)

    if ckFlag == True:
        return render_template('dashboard.html',uname = uname)
    elif ckFlag == False:
        return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        res = request.json[0]
        uname = res['uname']
        passwd = res['passwd']
        result = setlogininfo(uname,passwd)
        if result == None:
            return 444 #ログインエラーのレス
        token = result
        tokenflag = checkToken(token=token)
        if(tokenflag == True):
            pass
        elif(tokenflag == False):
            return 445 #トークンが無効
        
        return render_template('dashboard.html',uname=uname)
    
    elif request.method == 'GET':
        token = request.cookies.get('token',None)
        #token = None
        if token == None:
            return render_template('login.html')
        
        return redirect('/')
    

app.run(port=8080,host="0.0.0.0",debug=True)