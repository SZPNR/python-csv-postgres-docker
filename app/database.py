import pandas as pd
import sqlalchemy as db
import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.engine = db.create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')
            self.connection = self.engine.connect()
            print("Connected to database successfully")
        except db.exc.SQLAlchemyError as connection_error:
            print("Error connecting to database:", connection_error)

    def execute_query(self, query):
        try:
            result = self.connection.execute(db.text(query))
            rows = result.fetchall()
            result.close()
            print("Query executed successfully")
            return pd.DataFrame(rows, columns=result.keys())
        except db.exc.SQLAlchemyError as e:
            print("Error executing query:", e)
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
