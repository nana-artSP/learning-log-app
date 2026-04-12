from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime
import os


# -----------------
#  アプリ初期設定
# -----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------
#  データモデル定義
# -----------------
class StudyLog(BaseModel):
    subject: str
    minutes: int
    date: str
    start_time: str
    end_time: str


class StudyLogUpdate(BaseModel):
    subject: str
    minutes: int
    date: str
    start_time: str
    end_time: str


# -----------------
#  学習ログ一覧取得
# -----------------
@app.get("/study/all")
def get_all_logs():
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("SELECT id, subject, minutes, date, start_time, end_time FROM study_logs")
    rows = cur.fetchall()
    conn.close()

    return [
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


# -----------------
#  学習ログ追加
# -----------------
@app.post("/study/add")
def add_study_log(log: StudyLog):
    print("使用中のDBパス:", os.path.abspath("study.db"))

    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO study_logs (subject, minutes, date, start_time, end_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        log.subject,
        log.minutes,
        log.date,
        log.start_time,
        log.end_time,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return {"status": "ok", "message": "学習ログを追加しました！"}


# -----------------
#  学習ログ詳細取得
# -----------------
@app.get("/study/{log_id}")
def get_study_log(log_id: int):
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute(
    "SELECT id, subject, minutes, date, start_time, end_time FROM study_logs WHERE id = ?",
    (log_id,)
)
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {"message": "not found"}

    return {
    "id": row[0],
    "subject": row[1],
    "minutes": row[2],
    "date": row[3],
    "start_time": row[4],
    "end_time": row[5]
}


# -----------------
#  学習ログ削除
# -----------------
@app.delete("/study/delete/{log_id}")
def delete_study_log(log_id: int):
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM study_logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()

    return {"status": "ok", "message": "学習ログを削除しました"}


# -----------------
#  学習ログ更新
# -----------------
@app.put("/study/update/{log_id}")
def update_study_log(log_id: int, log: StudyLogUpdate):
    conn = sqlite3.connect("study.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE study_logs
        SET subject = ?, minutes = ?, date = ?, start_time = ?, end_time = ?
        WHERE id = ?
    """, (
        log.subject,
        log.minutes,
        log.date,
        log.start_time,
        log.end_time,
        log_id
    ))

    conn.commit()
    conn.close()

    return {"status": "ok", "message": "学習ログを更新しました"}