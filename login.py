import userLoginLib

uname = input("ユーザー名:")
passwd = input("パスワード")

userLoginLib.user_login_console(uname=uname,passwd=passwd)
print("実行完了")