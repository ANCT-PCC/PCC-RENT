from flask import Flask, redirect, url_for, render_template, request,make_response,send_file
from flask_httpauth import HTTPDigestAuth
import dbc
import random,string
import json
import datetime
import itemSubmit

TOKEN_SIZE = 64 #トークンのサイズ
COOKIE_AGE = 1 #Cookieの有効期限(単位:h)
VERSION = 'ver.3.0'

conn = dbc.startConnection()

#初期化処理
def init(conn):
    #すべてのトークンを無効化
    command=f'''UPDATE {dbc.DB_NAME}.{dbc.TABLE_NAME_LOGIN} SET token = "NoToken" WHERE token != "NoToken"'''
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(dbc.INIT_SQL_COMMAND_1)
    c.execute(dbc.INIT_SQL_COMMAND_2)
    c.execute(dbc.INIT_SQL_COMMAND_3)
    conn.commit()
    res = dbc.sqlExecute(conn,True,command)
    print(f"\nアクセストークン初期化を実行\n")
    print(f"Response: {res}\n\n")

#ランダムトークン生成
def randomname(TOKEN_SIZE):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))

app = Flask(__name__)
app.config['SECRET_KEY'] = randomname(TOKEN_SIZE)
auth = HTTPDigestAuth()

try:
    with open('setting_files/admin_info.json','r',encoding='utf-8') as f:
     Admin = json.load(f)

except FileNotFoundError:
    print("[PCC-RENT] ERROR: setting_files/admin_info.json NOT FOUND.")
    exit()

@auth.get_password
def get_pw(id):
    return Admin.get(id)

@app.route('/',methods=['GET'])
def index():
    token = request.cookies.get('token')
    uname = request.cookies.get('uname')
    displayname = request.cookies.get('displayname')
    if token is None or uname is None or displayname is None:
        return redirect('/login')
    else:
        pwchangeFlag = dbc.ckpwdchange(uname=uname)
        if pwchangeFlag == 1:
            return redirect('/pwdchange')
        login_status = dbc.cktoken(conn,uname,token)
        if login_status[1] == True: #ログイン状態である
            return render_template('dashboard.html',uname = displayname,ver=VERSION)
        elif login_status[1] == False:
            return redirect('/login')
        
@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        res = request.json[0]
        uname = res['uname']
        passwd = res['passwd']
        
        uinfo = dbc.authUser(uname,passwd)
        if uinfo['login_status'] == 0 or uinfo['login_status'] == 2:
            token = randomname(TOKEN_SIZE=TOKEN_SIZE) #一意のトークン
            displayname = dbc.search_userinfo_from_name(uname)[3]
            if uinfo['login_status'] == 2:
                res = make_response(redirect('/pwdchange'))
            else:
                res = make_response(redirect('/'))

            expires = int(datetime.datetime.now().timestamp()) + 60*60*COOKIE_AGE
            res.set_cookie('token', token,expires=expires)
            res.set_cookie('uname', uname,expires=expires)
            res.set_cookie('displayname',displayname,expires=expires)
            
            #DBに新しいトークンを上書きと同時に
            #サブプロセスでタイマーを作動
            dbc.update_token(conn,uname,token)

            return res

        else:
            return "444",444
    
    elif request.method == 'GET':
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        if token is None:
            return render_template('login.html')
        else:
            ckflag = dbc.cktoken(conn,uname,token)
            if ckflag[1] == False:
                return render_template('login.html')
            elif ckflag[1] == True:
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
    res.delete_cookie('displayname')
    dbc.update_token(conn,uname,'NoToken')

    return res

@app.route('/user_settings',methods=['GET'])
def user_settings():

    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        return render_template('user_settings.html',uname=displayname,ver=VERSION)
        
@app.route('/pwdchange')
def pwdchange():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        return render_template('passwd_change.html',uname=displayname,ver=VERSION)
    
@app.route('/my_rental_list')
def my_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    login_status = dbc.cktoken(conn,uname,token)
    if login_status[1] != True:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('my_rental_list.html',uname=displayname,ver=VERSION)
    
@app.route('/pcc-items')
def pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    login_status = dbc.cktoken(conn,uname,token)
    if login_status[1] != True:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('pcc-items.html',uname=displayname,ver=VERSION)
    
@app.route('/members')
def members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    login_status = dbc.cktoken(conn,uname,token)
    if login_status[1] != True:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('members.html',uname=displayname,ver=VERSION)
    
@app.route('/show_members')
def show_members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
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
    displayname = request.cookies.get('displayname')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        res = dbc.sarch_rent_items(conn,displayname)
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rent']=str(res[flag][4])
            dict['deadline']=str(res[flag][5])
            dict['returned']=str(res[flag][6])
            dict['rental_id']=str(res[flag][7])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_all_rental_list')
def show_all_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        res = dbc.get_rent_items(conn)
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
    
@app.route('/show_pcc-items')
def show_pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        res = dbc.get_all_items(conn)
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
    
@app.route('/return_item',methods=['POST'])
def return_item():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        rental_id = request.json[0]['rental_id']
        userinfo = dbc.search_userinfo_from_name(uname)
        displayname = userinfo[3]
        
        res = dbc.return_item(conn,rental_id=rental_id,returnedby=displayname+' '+uname)
        if res == 0:
            return "OK",200
        else:
            return "ERROR",400
        
@app.route('/rental_item',methods=['POST'])
def rental_item():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    ckFlag = dbc.cktoken(conn,uname,token)
    if ckFlag[1] != True:
        return redirect('/login')
    else:
        item_number = request.json[0]['item_number']
        userinfo = dbc.search_userinfo_from_name(uname)
        item_name = dbc.search_iteminfo_from_number(conn,item_number)[0][1]
        use = '未記載'
        res = dbc.rent_item(conn,item_number,item_name,use,userinfo[3],uname)

        if res == 0:
            return "OK",200
        else:
            return "ERROR",400
        
@app.route('/admintools')
@auth.login_required
def admintools_top():
    return redirect('/admintools/top')

@app.route('/admintools/<string:page>')
@auth.login_required
def admintools(page):
    return render_template('admintools/'+page+'.html',ver=VERSION)
    
@app.route('/admintools/submititems/<string:mode>',methods=['POST'])
@auth.login_required
def submititems(mode):

    if mode == 'submit':
        submit_contents = str(request.json['content'])
        with open('itemList.csv','w',encoding='utf-8') as f:
            f.write(submit_contents)

        itemSubmit.itemSubmit(conn)
        return "OK"
    elif mode == 'delete':
        delete_contents = str(request.json['content'])
        with open('delitemList.csv','w',encoding='utf-8') as f:
            f.write(delete_contents)

        itemSubmit.itemDelete(conn)
        return "OK"
    else:
        return "404",404
    
@app.route('/admintools/db/sqlexecute',methods=['POST'])
@auth.login_required
def sqlexecute():
    sqlcmd = str(request.json['sqlcmd'])
    result = dbc.sqlExecute(conn,True,sqlcmd)
    data = {'content':result}
    return data['content'],200


init(conn)
app.run(port=8081,host="0.0.0.0",debug=True,threaded=True)