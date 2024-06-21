import sqlite3,json,datetime
import random,string
import json
import subprocess
import hashlib
import mysql.connector
import CAS_userLib

DB_SERVER = 'pcc-rent-db'
#DB_SERVER='127.0.0.1'
DB_NAME = 'pcc_rent'
DB_PASSWD = 'Kusopass'

TABLE_NAME_LOGIN = 'pcc_login'
TABLE_NAME_ITEMS = 'pcc_items'
TABLE_NAME_RENTALS = 'pcc_rental'

TOKEN_SIZE = 64
WEBHOOK_URL = 'https://discord.com/api/webhooks/1238851270597541888/krtdLGswv7LRx1KhqvQdRh2MR9xCGsSSROmoRikxD_FEeQ3gfU16OUzB1CPSko5OZDX9'

INIT_SQL_COMMAND_1 = f'''CREATE TABLE IF NOT EXISTS {DB_NAME}.{TABLE_NAME_LOGIN}(
    username VARCHAR(255) NOT NULL PRIMARY KEY,
    token TEXT
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'''

INIT_SQL_COMMAND_2 = f'''CREATE TABLE IF NOT EXISTS {DB_NAME}.{TABLE_NAME_ITEMS}(
    number VARCHAR(255) NOT NULL PRIMARY KEY,
    item_name TEXT,
    desc TEXT,
    resource TEXT,
    rental TEXT,
    picture TEXT,
    rental_id TEXT
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'''

INIT_SQL_COMMAND_3 = f'''CREATE TABLE IF NOT EXISTS {DB_NAME}.{TABLE_NAME_RENTALS}(
    number TEXT,
    item_name TEXT,
    use TEXT,
    rentby TEXT,
    rent TEXT,
    deadline TEXT,
    returned TEXT,
    rental_id VARCHAR(255) NOT NULL PRIMARY KEY
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'''

try:
    with open('setting_files/CAS_token.json','r',encoding='utf-8') as f:
     casToken = json.load(f)

except FileNotFoundError:
    print("[PCC-RENT] ERROR: setting_files/CAS_token.json NOT FOUND.")
    exit()

SYSTEM_TOKEN = casToken['token']
print(f"PCC-CAS TOKEN : {SYSTEM_TOKEN}")

#MySQL接続
def startConnection():
    conn = mysql.connector.connect(
        host=DB_SERVER,
        user='root',
        password=DB_PASSWD,
        database=DB_NAME,
        port='3306'
    )
    return conn

#MySQL切断
def closeConnection(conn):
    conn.close()

#汎用SQL実行
def sqlExecute(conn,mode:bool,sql:str):
    c = conn.cursor()
    c.execute(sql)
    res=c.fetchall()

    if mode == True:
        #書き込みモード
        print("\n[Notice]\t書き込みモードで実行しました")
        conn.commit()
    else:
        print("\n[Notice]\t書き込みモードで実行していません")
        pass

    c.close()
    return res

def discord_message(message:str,uname:str):
    command = ["python","send_discord.py",message,uname]
    subprocess.Popen(command)
    

#################################################################

#ユーザー関連

#################################################################

#PCC-CASより、ユーザー登録情報を検索(ユーザー名から)
def search_userinfo_from_name(name:str):
    res = CAS_userLib.getUserInfo(name,SYSTEM_TOKEN)
    return res[1]


#全ユーザー登録情報一覧
def get_all_users():
    res = CAS_userLib.getAllUserInfo(SYSTEM_TOKEN)
    return res[1] #ユーザー登録情報を配列として返す

#有効なトークンの有効性検証結果とユーザ名の応答        
def cktoken(conn,name:str,token:str):
    c=conn.cursor()
    c.execute(f'''SELECT * from {DB_NAME}.{TABLE_NAME_LOGIN} WHERE token = "{token}"''')
    res = c.fetchall()
    conn.commit()
    c.close()

    if len(res) == 0:
        return "NoUsername",False
    else:
        return name,True

#トークン更新
def update_token(uname:str,new_token:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql1 = f'''
        UPDATE "pcc-users" SET accessToken = "{new_token}" WHERE name = "{uname}"
    '''
    c.execute(sql1)
    conn.commit()

#ユーザのパスワード未変更を検出
def ckpwdchange(uname:str):
    res = search_userinfo_from_name(uname)
    if len(res) == 0:
        return 1
    uname_hash = hashlib.sha256(uname.encode('utf-8')).hexdigest()
    applied_passwd = res[0][5] #現在設定されているパスワード
    old_temp_passwd_hash = uname_hash #初期パスワード(改定前)
    new_temp_passwd = 'Kusopass@'+uname[1:]
    new_temp_passwd_hash = hashlib.sha256(new_temp_passwd.encode('utf-8')).hexdigest() #初期パスワード(改定後)

    if applied_passwd == old_temp_passwd_hash or applied_passwd == new_temp_passwd_hash:
        return 1 #パスワードが未変更
    else:
        return 0


#################################################################

#備品関連

#################################################################

#備品を登録する
def create_new_item(number:str,name:str,desc:str,resource:str,rental:str,picture:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(INIT_SQL_COMMAND_2)
    data = (number,name,desc,resource,rental,picture,'NoSet')
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-items" VALUES(?,?,?,?,?,?,?)
        EXCEPT
        SELECT * FROM "pcc-items" WHERE number == '{number}'
        '''
    c.execute(sql,data)
    #コミット(変更を反映)
    conn.commit()
    c.close()
    return 0

#備品を削除
def delete_item(number:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #備品削除
    c.execute(f'''DELETE FROM "pcc-items" WHERE number == '{number}' ''')
    conn.commit()
    c.close()

#備品を検索(名前から)
def search_iteminfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE item_name == '{name}' '''):
        res = json.loads(json.dumps(i,ensure_ascii=False))
    conn.close()
    return res #備品のレコードを配列として返す

#備品を検索(備品番号から)
def search_iteminfo_from_number(number:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE number == '{number}' '''):
        res = json.loads(json.dumps(i,ensure_ascii=False))
    conn.close()
    return res #備品のレコードを配列として返す

#ユーザの貸し出し備品を検索(備品番号から)
def search_userrentalinfo_from_number(number:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE number == '{number}' ''')
    res = c.fetchall()
    conn.close()
    return res #備品のレコードを配列として返す
    

#備品を借用(履歴に記録)
def rent_item(item_number:str,item_name:str,use:str,rentby:str,uname:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(INIT_SQL_COMMAND_3)
    #res =[]
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE number == '{item_number}' AND returned == '貸し出し中' AND rental_id == 'NotSet' ''')
    res = c.fetchall()

    if len(res)==0:
        sql = f'''
            INSERT INTO "pcc-rental" VALUES(?,?,?,?,?,?,?,?)
        '''
        timestamp = datetime.datetime.now()
        deadline = timestamp + datetime.timedelta(days=14)
        rental_id = ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))
        data = (item_number,item_name,use,rentby,timestamp.strftime('%Y年%m月%d日 %H:%M'),deadline.strftime('%Y年%m月%d日'),'貸し出し中',rental_id)
        c.execute(sql,data)
        sql2 = f'''
            UPDATE "pcc-items" SET rental = '{rentby}' WHERE number = '{item_number}'
        '''
        sql3 = f'''
            UPDATE "pcc-items" SET rental_id = '{rental_id}' WHERE number = '{item_number}'
        '''
        c.execute(sql2)
        c.execute(sql3)
        conn.commit()
        conn.close()

        #Discord 借用通知
        message = f"備品番号{item_number}:「{item_name}」を **借用** しました"
        
        userinfo = search_userinfo_from_name(uname)[0]
        displayname = userinfo[0]
        discord_message(message,displayname+' '+uname)

        return 0
    else:
        print(f"借用が重複している可能性があります: {item_number}")
        conn.commit()
        conn.close()

        return -1

#備品を返却(履歴に記録)
def return_item(rental_id:str,returnedby:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.datetime.now()
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE rental_id = "{rental_id}"''')
    info = c.fetchall()
    c.execute(f'''UPDATE "pcc-rental" SET returned = '返却済み:<br>{timestamp.strftime('%Y年%m月%d日 %H:%M')}' WHERE rental_id == '{rental_id}' ''')
    
    sql3 = f'''
        UPDATE "pcc-items" SET rental = 'なし' WHERE rental_id = '{rental_id}'
    '''
    sql4 = f'''
        UPDATE "pcc-items" SET rental_id = 'NoSet' WHERE rental_id = '{rental_id}'
    '''
    c.execute(sql3)
    c.execute(sql4)
    conn.commit()
    conn.close()

    #Discord 返却通知
    item_number = info[0][0]
    item_name = info[0][1]
    message = f"備品番号{item_number}: 「{item_name}」を **返却** しました"
    discord_message(message,returnedby)

    return 0

#借りられている備品を検索
def get_rent_items():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-rental"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す

#ユーザが借りている備品を検索
def sarch_rent_items(uname:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = f'''
        SELECT * FROM "pcc-rental" WHERE rentby == "{uname}"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す

#全備品登録情報一覧
def get_all_items():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-items"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す