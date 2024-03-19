import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

class PostgreSQLManager:
    def __init__(self, port=5432):
        self.host = os.getenv("PG_HOST")
        self.dbname = os.getenv("PG_DB")
        self.user = os.getenv("PG_USER")
        self.password = os.getenv("PG_PASS")
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            self.cur = self.conn.cursor()
            print("Connected to PostgreSQL database!")
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)

    def create_table(self, table_name, column_name):
        if self.cur:
            try:
                self.cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, {column_name} VARCHAR(128))"""
                )
                self.conn.commit()
                print(f"Table '{table_name}' created successfully!")
            except psycopg2.Error as e:
                print("Error creating table:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def store(self, table_name, column_name, value):
        if self.cur:
            try:
                self.cur.execute(
                    f"""INSERT INTO {table_name} ({column_name}) VALUES (%s)""",
                    (value,),
                )
                self.conn.commit()
                print("Value stored successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error storing value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def update(self, table_name, column_name, id_value, new_value):
        if self.cur:
            try:
                self.cur.execute(
                    f"""UPDATE {table_name} SET {column_name} = %s WHERE id = %s""",
                    (new_value, id_value),
                )
                self.conn.commit()
                print("Value updated successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error updating value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def delete(self, table_name, column_name, id_value):
        if self.cur:
            try:
                self.cur.execute(
                    f"""DELETE FROM {table_name} WHERE {column_name} = %s""",
                    (id_value,),
                )
                self.conn.commit()
                print("Value deleted successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error deleting value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def close_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            print("Connection to PostgreSQL database closed.")

    def delete_table(self, table_name):
        if self.cur:
            try:
                self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
                self.conn.commit()
                print(f"Table '{table_name}' deleted successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error deleting table:", e)
        else:
            print("Not connected to the database. Call connect() first.")


# if __name__ == "__main__":
#     pg_manager = PostgreSQLManager()
#     pg_manager.connect()
#     pg_manager.create_table("user_message_inbox_duplicate", "value")
#     pg_manager.close_connection()