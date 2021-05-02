import sqlite3


class SQLighter:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()


    def select_all(self):
        arr = self.cur.execute("select * from music").fetchall()
        return arr

    def select_single(self, rownum):
        arr = self.cur.execute("select * from music where rowsnum = ?", (rownum,)).fetchone()
        return arr

    def count_rows(self):
        ans = self.cur.execute("select COUNT(*) from music").fetchone()[0]
        return ans

    def close(self):
        self.conn.close()
