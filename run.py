from flask import Flask, redirect, url_for, render_template, request,make_response
from datetime import timedelta #時間情報を用いるため
from datetime import datetime
import dbc
import random,string
#from flask_cors import CORS


TOKEN_SIZE = 64
app = Flask(__name__)

app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=5) # -> 5分 #(days=5) -> 5日保存

#ランダムトークン生成
def randomname(TOKEN_SIZE):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))

#ログイン時にトークンを発行
def setlogininfo(uid:str,passwd:str):

    uinfo = dbc.search_userinfo_from_name(uid)
    if len(uinfo) != 0:
        print(f"{uinfo[0][4]}")
        if(uinfo[0][4] == passwd):
            passwd_flag = True
        else:
            passwd_flag = False

        if passwd_flag == True: #パスワードがあっている
            print(f"\nパスワードがあっている時の処理\n")
            token = randomname(TOKEN_SIZE=TOKEN_SIZE) #一意のトークン
            res = make_response("Setting limited cookie")
            expire_date = datetime.now() + timedelta(hours=1)
            res.set_cookie('token', token, expires=expire_date, secure=True, httponly=True)
            res.set_cookie('uname', uid, expires=expire_date, secure=True, httponly=True)
            
            #DBに新しいトークンを上書きと同時に
            #サブプロセスでタイマーを作動
            dbc.update_token(uid,token)

            return res , token #ログインが正常であれば、トークンを発行
            #voidToken = token
        else:
            return "Nodata","Nodata"
    else:
        return "Nodata","Nodata"

@app.route('/',methods=['GET'])
def index():
    token = request.cookies.get('token')
    uname = request.cookies.get('uname')
    #token = 'abcd1234'
    print(f"uname:{uname} , token={token}")
    if token is None or uname is None:
        return redirect('/login')
    else:
        ckFlag,uname,login_status = dbc.cktoken(uname,token)
        if ckFlag == True: #ログイン状態である
            return render_template('dashboard.html',uname = uname)
        elif ckFlag == False:
            return redirect('/login')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        res = request.json[0]
        uname = res['uname']
        passwd = res['passwd']
        print(f"{uname} , {passwd}")
        
        result,token=setlogininfo(uname,passwd)
        #result = None
        print(f"\ntoken={token}\nresult={result}\n")
        if result == "Nodata" or token is None or result is None:
            print("\nDEBUG\n")

            return "444",444 #ログインエラーのレス
        else:
            tokenflag , uname , login_sta = dbc.cktoken(uname,str(token))
            
            if(tokenflag == True):
                pass
            elif(uname == "Not Submit"):
                return "446",446 #ユーザ登録なし
            elif(tokenflag == False):
                #return "445",445 #トークンが無効
                pass
            
            return redirect('/')
    
    elif request.method == 'GET':
        token = request.cookies.get('token')
        #token = None
        if token == None:
            return render_template('login.html')
        
        return redirect('/')

@app.after_request
def set_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Method'] = 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS'  # noqa: E501
    response.headers['Access-Control-Allow-Headers'] = 'Content-type,Accept,X-Custom-Header'  # noqa: E501
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response


app.run(port=8080,host="0.0.0.0",debug=True)