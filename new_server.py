from flask import Flask, redirect, url_for, render_template, request, session #session追加
from datetime import timedelta #時間情報を用いるため

app = Flask(__name__)

app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=5) # -> 5分 #(days=5) -> 5日保存

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
  #データベースに情報を送るとき
  if request.method == "POST":
    session.permanent = True  # <--- makes the permanent session
    user = request.form["nm"] #ユーザー情報を保存する
    session["user"] = user #sessionにuser情報を保存
    return redirect(url_for("user"))
  else: #情報を受け取るとき
    if "user" in session: #sessionにユーザー情報があったとき
      return redirect(url_for("user")) #userページに遷移
    return render_template("login.html") #sessionにユーザー情報がなかったときはloginページに遷移

@app.route("/user")
def user():
  if "user" in session:
    user = session["user"] #sessionからユーザー情報をとってくる
    return f"<h1>{user}</h1>"
  else:
    return redirect(url_for("login"))

@app.route("/logout") #ログアウトする
def logout():
  session.pop("user", None) #削除
  return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(debug=True)
