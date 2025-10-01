import sqlite3
import os


class DBUtils:
    def __init__(self, db):
        self.db = db

        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def create_table(self, ddl):
        self.cursor.executescript(ddl)



