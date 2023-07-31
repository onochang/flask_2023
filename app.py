# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request, redirect
# sqlite3をインポート
import sqlite3
# Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)

# /にアクセスされた時に処理を返す（ルーティング）
# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<name>")
def greet(name):
    return name + "さん、こんにちは！"

@app.route('/add')
def add_get():
    return render_template("add.html")

@app.route('/add', methods=["POST"])
def add_post():
    task = request.form.get("task")
    print(task)
    # データベースに接続
    conn = sqlite3.connect("myTask.db")
    # データベースを操作するための準備
    c = conn.cursor()
    # SQLを実行
    c.execute("insert into task values (null, ?)", (task,))
    # データベースを更新
    conn.commit()
    # データベースの接続を終了
    c.close()
    return redirect("/list")

@app.route("/list")
def list_get():
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("select id, task from task")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id":row[0], "task":row[1]})
    c.close()
    return render_template("list.html", task_list = task_list)

@app.route("/edit/<int:task_id>")
def edit_get(task_id):
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("select task from task where id = ?",(task_id,))
    task = c.fetchone()
    print(task)
    c.close()
    task=task[0]
    return render_template("edit.html", task = task, task_id = task_id)

@app.route("/edit", methods=["POST"])
def edit_post():
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

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("delete from task where id = ?", (task_id,))
    conn.commit()
    c.close()
    return redirect("/list")

@app.route('/regist')
def regist_get():
    return render_template("/regist.html")

@app.route('/login')
def login_get():
    return render_template("/login.html")

# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)