from flask import Flask, request, jsonify, render_template, session, redirect
import sqlite3
import bcrypt
from flask_cors import CORS
import requests



app = Flask(__name__)
app.secret_key = "secret_key_here"   # セッションに必須
CORS(app)

# -----------------
#  新規登録
# -----------------
@app.post("/signup")
def signup():
    data = request.json
    email = data["email"]
    password = data["password"]

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hashed_pw))
        conn.commit()
        return jsonify({"message": "ok"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "exists"})
    finally:
        conn.close()


# -----------------
#  ログイン
# -----------------
@app.post("/login")
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"message": "no_user"})

    hashed_pw_from_db = row[0]

    if bcrypt.checkpw(password.encode(), hashed_pw_from_db):
        session["username"] = email  # ←ログイン状態記録！
        return jsonify({"message": "ok"})
    else:
        return jsonify({"message": "wrong_pw"})


@app.get("/login")
def login_page():
    return render_template("py.login.html")

@app.get("/signup_page")
def signup_page():
    return render_template("py.signup.html")

# -----------------
#  プロフィールページ
# -----------------
@app.get("/profile")
def profile_page():
    if "username" not in session:
        return redirect("/login")

    return render_template("py.profile.html")

# -----------------
# 編集画面開く
# -----------------

@app.get("/study_logs/edit/<int:log_id>")
def edit_study_log_page(log_id):
    res = requests.get(f"http://127.0.0.1:8000/study/{log_id}")
    log = res.json()
    return render_template("study_edit.html", log=log)


# -----------------
# 更新処理
# -----------------

@app.post("/study_logs/update/<int:log_id>")
def update_study_log_page(log_id):
    subject = request.form["subject"]
    minutes = int(request.form["minutes"])
    date = request.form["date"]

    data = {
        "subject": subject,
        "minutes": minutes,
        "date": date
    }

    requests.put(f"http://127.0.0.1:8000/study/update/{log_id}", json=data)
    return redirect("/study_logs")

# -----------------
# 追加
# -----------------

@app.get("/study_logs/add")
def study_add_page():
    return render_template("study_input.html")

# -----------------
#  ログアウト
# -----------------
@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -----------------
#  学習ログ呼び出し
# -----------------

@app.get("/study_logs")
def study_logs():
    res = requests.get("http://127.0.0.1:8000/study/all")
    logs = res.json()
    return render_template("study_logs.html", logs=logs)

# -----------------
#  削除
# -----------------

@app.post("/study_logs/delete/<int:log_id>")
def delete_study_log_page(log_id):
    requests.delete(f"http://127.0.0.1:8000/study/delete/{log_id}")
    return redirect("/study_logs")


# -----------------
#  Flask起動（必ず最後）
# -----------------
if __name__ == "__main__":
    app.run(debug=True)

