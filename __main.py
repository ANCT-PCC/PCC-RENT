from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# シンプルなユーザーデータの辞書(適宜DB接続等実施してください)
users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'}
}

@app.route("/")
def main_page():
    return redirect(url_for('login'))

#ログイン処理
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 画面で入力された情報を取得
        username = request.form['username']
        password = request.form['password']

        # ログイン可否を判定
        if username in users and users[username]['password'] == password:
            session['username'] = username

            # ログイン成功でdashbord.htmlを返す
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    # GETの場合はログイン画面へ戻す
    return render_template('login.html')

#URL直接参照の場合
@app.route('/dashboard')
def dashboard():
    # ログインしている場合はdashbord.htmlへ
    if 'username' in session:
        return render_template('dashbord.html')
    else:
        return redirect(url_for('login'))


#ログアウト機能
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=443,debug=True,host='0.0.0.0')