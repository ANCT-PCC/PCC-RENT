from flask import Flask, redirect, url_for, render_template, request,make_response
import dbc
import random,string
import sqlite3
import json

TOKEN_SIZE = 64

app = Flask(__name__)

#初期化処理
def init():
    command='''UPDATE "pcc-users" SET accessToken = "NoToken" WHERE accessToken != "NoToken"'''
    conn = sqlite3.connect(dbc.DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(dbc.INIT_SQL_COMMAND)
    c.execute(dbc.INIT_SQL_COMMAND_2)
    c.execute(dbc.INIT_SQL_COMMAND_3)
    conn.commit()
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
            print(f"{uinfo[0][5]}")
            if(uinfo[0][5] == passwd):
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
            if login_sta == 1 or login_sta==2 or login_sta==0:
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

@app.route('/user_settings',methods=['GET','POST'])
def user_settings():

    if request.method == 'POST':
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')

        uname,login_status = dbc.cktoken(uname,token)
        if login_status != 3:
            return redirect('/login')
        else:
            currentPWD = request.json[0]['currentPWD']
            newPWD = request.json[0]['newPWD']

            uinfo = dbc.search_userinfo_from_name(uname)
            if uinfo[0][5] != currentPWD:
                return "444",444
            elif uinfo[0][5] == currentPWD:
                #パスワード変更処理
                previnfo,newinfo = dbc.update_user_info(uname,'passwd',newPWD)
                newuinfo = dbc.search_userinfo_from_name(uname)
                print(newuinfo[0][4])
                return "415",415


    else:

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
    
@app.route('/members')
def members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        return render_template('members.html',uname=uname)
    
@app.route('/show_members')
def show_members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_all_users()
        member_info = []

        for flag in range(len(res)):
            dict = {}
            dict['display']=str(res[flag][0])
            dict['uname']=str(res[flag][1])
            dict['grade']=str(res[flag][9])
            dict['class']=str(res[flag][10])
            dict['discord']=str(res[flag][11])
            member_info.append(dict)

        return json.dumps(member_info)
    
@app.route('/show_my_rental_list')
def show_my_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.sarch_rent_items(uname)
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rent']=str(res[flag][4])
            dict['deadline']=str(res[flag][5])
            dict['returned']=str(res[flag][6])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_all_rental_list')
def show_all_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_rent_items()
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rentby']=str(res[flag][3])
            dict['rent']=str(res[flag][4])
            dict['deadline']=str(res[flag][5])
            dict['returned']=str(res[flag][6])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_all_rental_history')
def show_all_rental_history():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_rent_history()
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rentby']=str(res[flag][3])
            dict['type']=str(res[flag][4])
            dict['timestamp']=str(res[flag][5])
            dict['deadline']=str(res[flag][6])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_pcc-items')
def show_pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_all_items()
        item_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['desc']=str(res[flag][2])
            dict['resource']=str(res[flag][3])
            dict['rental']=str(res[flag][4])
            dict['picture']=str(res[flag][5])
            item_info.append(dict)

        return json.dumps(item_info)

init()
app.run(port=8080,host="0.0.0.0",debug=True)