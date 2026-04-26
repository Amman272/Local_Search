import sqlite3
conn= sqlite3.connect("file_id.db")

cursor =conn.cursor()

def init_db():
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS FILE_ID (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   FILENAME TEXT unique)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS INDEXING
                   (WORD TEXT,
                   FILE_ID INTEGER,
                   FREQUENCY INTEGER,
                   primary key (WORD,FILE_ID))""")
    conn.commit()

def Files(file_name):
    cursor.execute("""INSERT OR IGNORE INTO FILE_ID(FILENAME) VALUES(?)""",(file_name,))
    print(f"file:{file_name} has been added ")
    conn.commit()
    return cursor.execute("SELECT id FROM FILE_ID WHERE FILENAME=?", (file_name,)).fetchone()[0]

def tokensation(file_id, word):
    cursor.execute("""INSERT INTO INDEXING (WORD,FILE_ID,FREQUENCY)
                     VALUES(?,?,?)
                    on conflict (WORD,FILE_ID)
                   DO UPDATE SET FREQUENCY= FREQUENCY+1
                   """,(word,file_id,1))

def commit():
    conn.commit()
def search(words):
    placeholders = ",".join(["?"] * len(words))

    query = f"""
    SELECT FILE_ID.FILENAME, SUM(INDEXING.FREQUENCY) as score
    FROM INDEXING
    JOIN FILE_ID ON INDEXING.FILE_ID = FILE_ID.id
    WHERE INDEXING.WORD IN ({placeholders})
    GROUP BY INDEXING.FILE_ID
    HAVING COUNT(DISTINCT INDEXING.WORD) = ?
    ORDER BY score DESC
    """

    cursor.execute(query, (*words, len(words)))
    return cursor.fetchall()