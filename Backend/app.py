from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.get("/start/{nickname}")
def start_quiz(nickname: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        nickname TEXT PRIMARY KEY,
        counter INT
    )
    """)

    cur.execute("SELECT counter FROM users WHERE nickname=%s",(nickname,))
    result = cur.fetchone()

    if result:
        counter = result[0] + 1
        cur.execute("UPDATE users SET counter=%s WHERE nickname=%s",(counter,nickname))
    else:
        counter = 1
        cur.execute("INSERT INTO users VALUES(%s,%s)",(nickname,counter))

    conn.commit()
    cur.close()
    conn.close()

    return {"counter":counter}
