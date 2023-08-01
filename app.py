# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request, redirect, session
# sqlite3をインポート
import sqlite3
# Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)

app.secret_key = "SUNABACO2023"

# /にアクセスされた時に処理を返す（ルーティング）
# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("index.html")

@app.route("/<name>")
def greet(name):
    return name + "さん、こんにちは！"

@app.route('/add')
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/")

@app.route('/add', methods=["POST"])
def add_post():
    if "user_id" in session:
        user_id = session["user_id"][0]
        task = request.form.get("task")
        print(task)
        # データベースに接続
        conn = sqlite3.connect("myTask.db")
        # データベースを操作するための準備
        c = conn.cursor()
        # SQLを実行
        c.execute("insert into task values (null, ?, ?)", (task, user_id))
        # データベースを更新
        conn.commit()
        # データベースの接続を終了
        c.close()
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/list")
def list_get():
    if "user_id" in session:
        user_id = session["user_id"][0]
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("select name from users where id = ?", (user_id,))
        user_name = c.fetchone()[0]
        c.execute("select id, task from task where user_id = ?", (user_id,))
        task_list = []
        for row in c.fetchall():
            task_list.append({"id":row[0], "task":row[1]})
        c.close()
        return render_template("list.html", task_list = task_list, user_name = user_name)
    else:
        return redirect("/")

@app.route("/edit/<int:task_id>")
def edit_get(task_id):
    if "user_id" in session:
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("select task from task where id = ?",(task_id,))
        task = c.fetchone()
        print(task)
        c.close()
        task=task[0]
        return render_template("edit.html", task = task, task_id = task_id)
    else:
        return redirect("/")

@app.route("/edit", methods=["POST"])
def edit_post():
    if "user_id" in session:
        # フォームからtaskのidを取得
        task_id = request.form.get("task_id")
        # フォームから修正後の入力内容を取得
        task = request.form.get("task")
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("update task set task = ? where id = ?", (task, task_id))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" in session:
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("delete from task where id = ?", (task_id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/")

@app.route('/regist')
def regist_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("/regist.html")

@app.route("/regist", methods=["POST"])
def regist_post():
    # フォームから名前を取得
    name = request.form.get("name")
    # フォームからパスワードを取得
    password = request.form.get("password")
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("insert into users values(null, ?, ?)",(name, password))
    conn.commit()
    c.close()
    return redirect("/login")

@app.route('/login')
def login_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("/login.html")

@app.route("/login", methods=["POST"])
def login_post():
    # フォームから名前を取得
    name = request.form.get("name")
    # フォームからパスワードを取得
    password = request.form.get("password")
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("select id from users where name = ? and password = ?",(name, password))
    id = c.fetchone()
    c.close()
    if id is None:
        return redirect("/login")
    else:
        session["user_id"] = id
        return redirect("/list")
    
@app.route("/logout")
def logout():
    session.pop('user_id',None)
    return redirect("/")


# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)