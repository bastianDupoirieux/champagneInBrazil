import sqlite3
import sqlalchemy as db
from pathlib import Path


class DBUtils:
    def __init__(self, connection_string:str):
        self.connection_string = connection_string

        db_path = Path(connection_string)
        if not db_path.is_file():
            raise FileNotFoundError(f"File {db_path} does not exist")

        self.engine = db.create_engine(self.connection_string) #create the database engine





