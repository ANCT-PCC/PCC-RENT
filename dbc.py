import sqlite3

DB_NAME = 'pcc-rent.db'

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

if __name__ == '__main__':
    #create_new_user('齋藤直人','s203120@edu.asahikawa-nct.ac.jp',0,'Minecraft7010')
    #delete_user("齋藤直人")
    search_userinfo_from_name("齋藤直人")