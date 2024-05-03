from flask import Flask, redirect, url_for, render_template, request,make_response
import dbc
import random,string

TOKEN_SIZE = 64

app = Flask(__name__)

#初期化処理
def init():
    command='''UPDATE "pcc-users" SET accessToken = "NoToken" WHERE accessToken != "NoToken"'''
    res = dbc.sqlExecute(1,command)
    print(f"\nアクセストークン初期化を実行\n")
    print(f"Response: {res}\n\n")

#ランダムトークン生成
def randomname(TOKEN_SIZE):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))

@app.route('/',methods=['GET'])
def index():
    token = request.cookies.get('token')
    uname = request.cookies.get('uname')
    print(f"uname:{uname} , token={token}")
    if token is None or uname is None:
        return redirect('/login')
    else:
        uname,login_status = dbc.cktoken(uname,token)
        if login_status == 3: #ログイン状態である
            return render_template('dashboard.html',uname = uname)
        elif login_status == 1 or login_status == 2:
            return redirect('/login')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        res = request.json[0]
        uname = res['uname']
        passwd = res['passwd']
        print(f"{uname} , {passwd}")
        
        uinfo = dbc.search_userinfo_from_name(uname)
        if len(uinfo) != 0:
            print(f"{uinfo[0][4]}")
            if(uinfo[0][4] == passwd):
                passwd_flag = True
            else:
                passwd_flag = False

            if passwd_flag == True: #パスワードがあっている
                print(f"\nパスワードがあっている時の処理\n")
                token = randomname(TOKEN_SIZE=TOKEN_SIZE) #一意のトークン
                res = make_response(redirect('/'))
                res.set_cookie('token', token)
                res.set_cookie('uname', uname)
                
                #DBに新しいトークンを上書きと同時に
                #サブプロセスでタイマーを作動
                dbc.update_token(uname,token)

            else:
                token="Nodata"
                uname="Nodata"
                return "444",444
        else:
            token="Nodata"
            uname="Nodata"
            print(f"\ntoken={token}\nresult={res}\n")
            if res == "Nodata" or token is None or res is None:
                print("\nDEBUG\n")

                return "444",444 #ログインエラーのレス
            else:
                uname , login_sta = dbc.cktoken(uname,str(token))
                
                if(login_sta == 3):
                    pass
                elif(uname == "Not Submit"):
                    return "446",446 #ユーザ登録なし
                elif(login_sta == 2):
                    #return "445",445 #トークンが無効
                    pass
                
        return res
    
    elif request.method == 'GET':
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        if token is None:
            return render_template('login.html')
        else:
            uname,login_sta = dbc.cktoken(uname,token)
            if login_sta == 1 or login_sta==2:
                return render_template('login.html')
            elif login_sta == 3:
                return redirect('/')

@app.after_request
def set_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Method'] = 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS'  # noqa: E501
    response.headers['Access-Control-Allow-Headers'] = 'Content-type,Accept,X-Custom-Header'  # noqa: E501
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/logout')
def logout():
    uname=request.cookies.get('uname')
    res=make_response(redirect('/login'))
    res.delete_cookie('token')
    res.delete_cookie('uname')
    dbc.update_token(uname,'NoToken')

    return res

@app.route('/user_settings')
def user_settings():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        return render_template('user_settings.html',uname=uname)
    
@app.route('/my_rental_list')
def my_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        return render_template('my_rental_list.html',uname=uname)
    
@app.route('/pcc-items')
def pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        return render_template('pcc-items.html',uname=uname)

init()
app.run(port=8080,host="0.0.0.0",debug=True)