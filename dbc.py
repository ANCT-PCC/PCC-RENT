import sqlite3,json,datetime,numpy as np

DB_NAME = 'pcc-rent.db'

#################################################################

#ユーザー関連

#################################################################

#新規ユーザを作成する
def create_new_user(name:str,email:str,isAdmin:int,passwd:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute('''CREATE TABLE IF NOT EXISTS "pcc-users"(name,email,isAdmin,solt,passwd,activate_flag,uuid,accessToken) ''')
    solt = 'not set'
    data = (name,email,isAdmin,solt,passwd,0,'not set','NoToken')
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-users" VALUES(?,?,?,?,?,?,?,?)
        EXCEPT
        SELECT * FROM "pcc-users" WHERE name == '{name}'
        '''
    c.execute(sql,data)
    #コミット(変更を反映)
    conn.commit()
    c.close()
    return 0

#ユーザーを削除
def delete_user(name:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #ユーザー削除
    c.execute(f'''DELETE FROM "pcc-users" WHERE name == "{name}" ''')
    conn.commit()
    c.close()

#ユーザー登録情報を検索(ユーザー名から)
def search_userinfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute(f'''SELECT * FROM "pcc-users" WHERE name == "{name}" ''')
    res = c.fetchone()
    #レコードのフォーマット↓
    #name,email,isAdmin,solt,passwd,activate_flag,uuid
    conn.close()
    return res #ユーザーのレコードを配列として返す

#全ユーザー登録情報一覧
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-users"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #ユーザー登録情報を配列として返す

#ユーザー登録情報更新
def update_user_info(old_uname:str,new_name:str,passwd:str,column:str,new_data:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    prev_userinfo = search_userinfo_from_name(old_uname)

    sql1 = f'''
        UPDATE "pcc-users" SET "{column}" = "{new_data}" WHERE name = "{old_uname}"
    '''
    c.execute(sql1)
    conn.commit()
    
    new_userinfo = search_userinfo_from_name(old_uname)

    return prev_userinfo,new_userinfo

#有効なトークンの有効性検証結果とユーザ名の応答
def cktoken(token:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute(f'''SELECT * FROM "pcc-users" WHERE accessToken == "{token}" ''')
    res = c.fetchall()
    #レコードのフォーマット↓
    #name,email,isAdmin,solt,passwd,activate_flag,uuid,accessToken
    conn.close()

    if len(res) == 0:
        #print("ヒットなし")
        return False , "NoUname"
    elif str(res[0][7]) == "NoToken":
        #print("トークンなし")
        return False , "NoUname"
    else:
        uname = res[0][0]
        return True , str(uname)




#################################################################

#備品関連

#################################################################

#備品を登録する
def create_new_item(number:int,name:str,desc:str,resource:int,user:str,pic:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute('''CREATE TABLE IF NOT EXISTS "pcc-items"(Number,name,desc,resource,user,pic) ''')
    data = (number,name,desc,resource,user,pic)
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-items" VALUES(?,?,?,?,?,?)
        EXCEPT
        SELECT * FROM "pcc-items" WHERE name == '{name}'
        '''
    c.execute(sql,data)
    #コミット(変更を反映)
    conn.commit()
    c.close()
    return 0

#備品を削除
def delete_item(name:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #備品削除
    c.execute(f'''DELETE FROM "pcc-items" WHERE name == '{name}' ''')
    conn.commit()
    c.close()

#備品を検索(名前から)
def search_iteminfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE name == '{name}' '''):
        res = json.loads(json.dumps(i,ensure_ascii=False))
    conn.close()
    return res #備品のレコードを配列として返す
    

#備品を借用(履歴に記録)
def rent_item(name:str,user:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute('''CREATE TABLE IF NOT EXISTS "pcc-rental"(name,user,rent_date,return_date) ''')
    sql = '''
        INSERT INTO "pcc-rental" VALUES(?,?,?,?)
    '''
    rent_date = datetime.datetime.now()
    return_date = rent_date + datetime.timedelta(days=14)
    data = (name,user,rent_date.strftime('%Y年%m月%d日 %H:%M'),return_date.strftime('%Y年%m月%d日 %H:%M'))
    c.execute(sql,data)
    conn.commit()
    conn.close()

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