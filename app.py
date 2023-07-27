# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request
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
    name = "Onochang"
    area = "北海道江別市"
    profile = "SUNABACO EBETSUのスタッフです"
    return render_template("index.html", name = name, area = area, profile = profile)

@app.route("/<name>")
def greet(name):
    return name + "さん、こんにちは！"

# 2日目 -----------------------------------------------------
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
    return "入力を受け付けました。"

# ----------------------------------------------------------


# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)