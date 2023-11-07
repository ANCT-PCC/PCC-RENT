import sqlite3

DB_NAME = 'pcc-rent.db'

#################################################################

#ユーザー関連

#################################################################

#新規ユーザを作成する
def create_new_user(name:str,email:str,isAdmin:int,passwd:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute('''CREATE TABLE IF NOT EXISTS "pcc-users"(name,email,isAdmin,solt,passwd,activate_flag,uuid) ''')
    solt = 'not set'
    data = (name,email,isAdmin,solt,passwd,0,'not set')
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-users" VALUES(?,?,?,?,?,?,?)
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
    c.execute(f'''DELETE FROM "pcc-users" WHERE name == '{name}' ''')
    conn.commit()
    c.close()

#ユーザー登録情報を検索(ユーザー名から)
def search_userinfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()

    for i in c.execute(f'''SELECT * FROM "pcc-users" WHERE name == '{name}' '''):
        print(i)

#全ユーザー登録情報一覧
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-users"
    '''

    c.execute(sql)


#################################################################

#備品関連

#################################################################

#備品を登録する
def create_new_item(name:str,desc:str,resource:int,user:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute('''CREATE TABLE IF NOT EXISTS "pcc-items"(name,desc,resource,user) ''')
    data = (name,desc,resource,user)
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-items" VALUES(?,?,?,?)
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
def search_userinfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()

    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE name == '{name}' '''):
        print(i)