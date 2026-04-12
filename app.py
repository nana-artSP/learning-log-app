from flask import Flask, request, jsonify, render_template, session, redirect
from datetime import datetime
import sqlite3
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret_key_here"
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
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_pw)
        )
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
        session["username"] = email
        return jsonify({"message": "ok"})
    else:
        return jsonify({"message": "wrong_pw"})

# -----------------
#  ログインページ
# -----------------
@app.get("/login")
def login_page():
    return render_template("py.login.html")

# -----------------
#  新規登録ページ
# -----------------
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
#  学習ログ一覧
# -----------------
@app.get("/study_logs")
def study_logs():
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, subject, minutes, date, start_time, end_time
        FROM study_logs
    """)
    rows = cur.fetchall()
    conn.close()

    logs = [
        {
            "id": row[0],
            "subject": row[1],
            "minutes": row[2],
            "date": row[3],
            "start_time": row[4],
            "end_time": row[5]
        }
        for row in rows
    ]

    return render_template("study_logs.html", logs=logs)

# -----------------
#  学習ログ追加ページ
# -----------------
@app.get("/study_logs/add")
def study_add_page():
    return render_template("study_input.html")

# -----------------
#  学習ログ追加保存
# -----------------
@app.post("/study_logs/add")
def add_study_log_page():
    data = request.get_json()

    subject = data["subject"]
    minutes = int(data["minutes"])
    date = data["date"]
    start_time = data["start_time"]
    end_time = data["end_time"]

    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO study_logs (subject, minutes, date, start_time, end_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        subject,
        minutes,
        date,
        start_time,
        end_time,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "学習ログを追加しました！"})

# -----------------
#  学習ログ編集ページ
# -----------------
@app.get("/study_logs/edit/<int:log_id>")
def edit_study_log_page(log_id):
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, subject, minutes, date, start_time, end_time
        FROM study_logs
        WHERE id = ?
    """, (log_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        return "データが見つかりません", 404

    log = {
        "id": row[0],
        "subject": row[1],
        "minutes": row[2],
        "date": row[3],
        "start_time": row[4],
        "end_time": row[5]
    }

    return render_template("study_edit.html", log=log)

# -----------------
#  学習ログ更新
# -----------------
@app.post("/study_logs/update/<int:log_id>")
def update_study_log_page(log_id):
    subject = request.form["subject"]
    minutes = int(request.form["minutes"])
    date = request.form["date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]

    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE study_logs
        SET subject = ?, minutes = ?, date = ?, start_time = ?, end_time = ?
        WHERE id = ?
    """, (
        subject,
        minutes,
        date,
        start_time,
        end_time,
        log_id
    ))

    conn.commit()
    conn.close()

    return redirect("/study_logs")

# -----------------
#  学習ログ削除
# -----------------
@app.post("/study_logs/delete/<int:log_id>")
def delete_study_log_page(log_id):
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM study_logs WHERE id = ?", (log_id,))

    conn.commit()
    conn.close()

    return redirect("/study_logs")

# -----------------
#  ログアウト
# -----------------
@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -----------------
#  Flask起動
# -----------------
if __name__ == "__main__":
    app.run(debug=True)