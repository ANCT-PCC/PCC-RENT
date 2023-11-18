import dbc,os,json

#webログイン
def user_login_console(uname:str,passwd:str):
    res = dbc.search_userinfo_from_name(uname)
    #name,email,isAdmin,solt,passwd,activate_flag,uuid
    print(f"{uname} さんでログインしています。")
    print("=================================")

    while True:
        menustr = """

                1, ユーザー名の変更
                2,メールアドレスの変更
                3,パスワードの変更
                4,登録情報の閲覧

                0,ログアウトして終了
        """
        print(menustr)
        selection = input(">")

        if(selection == "1"):
            new_name = input("新しいユーザー名 > ")
            
            prev_data , new_data = dbc.update_user_info(uname=uname,passwd=passwd,column="name",new_data=new_name)

            print(f"変更前のデータ:\n{prev_data}")
            print(f"変更後のデータ:\n{new_data}")
            print("\ndone.\n")

        elif(selection == "2"):
            new_name = input("新しいメールアドレス > ")
            
            prev_data , new_data = dbc.update_user_info(uname=uname,passwd=passwd,column="email",new_data=new_name)

            print(f"変更前のデータ:\n{prev_data}")
            print(f"変更後のデータ:\n{new_data}")
            print("\ndone.\n")

        elif(selection == "3"):
            res = dbc.search_userinfo_from_name(uname)
            
            current_passwd = input("現在のパスワード >")
            if(current_passwd == res[0][4]):
                new_name = input("新しいパスワード > ")

                prev_data , new_data = dbc.update_user_info(uname=uname,passwd=passwd,column="email",new_data=new_name)

                print(f"変更前のデータ:\n{prev_data}")
                print(f"変更後のデータ:\n{new_data}")
            else:
                print("パスワードが間違っています。")
                os.wait(3)

            print("\ndone.\n")

        elif(selection == "4"):
            res = dbc.search_iteminfo_from_name(uname)
            if(res[2] == "1"):
                isAdmin = "管理者"
            else:
                isAdmin = "一般ユーザー"
            display = f'''
                    ユーザー名: {res[0][0]}
                    メールアドレス: {res[0][1]}
                    権限: {isAdmin}
            '''

            print(display)

        else:
            break