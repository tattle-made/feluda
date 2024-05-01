import psycopg2
from core.config import StoreConfig
from dotenv import load_dotenv
import os
load_dotenv()

class PostgreSQLManager:
    def __init__(self, param: StoreConfig, port=5432, ):
        self.host = os.getenv("PG_HOST")
        self.dbname = os.getenv("PG_DB")
        self.user = os.getenv("PG_USER")
        self.password = os.getenv("PG_PASS")
        self.port = port
        self.table_name = param.parameters.table_names[0]
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

    def create_trigger_function(self):
        if self.cur:
            try:
                prepared_stmt = """CREATE OR REPLACE FUNCTION trigger_set_timestamp()
                        RETURNS TRIGGER AS $$
                        BEGIN
                          NEW.updated_at = NOW();
                          RETURN NEW;
                        END;
                        $$ LANGUAGE plpgsql"""

                # create trigger function
                self.cur.execute(prepared_stmt)
                self.conn.commit()
                print("Trigger function created successfully!")
            except psycopg2.Error as e:
                print("Error creating trigger function:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def create_table(self, table_name):
        if self.cur:
            try:
                prepared_stmt = None
                if table_name == "user_message_inbox_duplicate":
                    prepared_stmt = """CREATE TABLE IF NOT EXISTS user_message_inbox_duplicate (
                            id SERIAL PRIMARY KEY,
                            value VARCHAR(128),
                            worker_name VARCHAR(128),
                            inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                            )"""
                elif table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = """CREATE TABLE IF NOT EXISTS user_message_inbox_perceptually_similar (
                            id SERIAL NOT NULL PRIMARY KEY, 
                            value VARCHAR(128), 
                            worker_name VARCHAR(128), 
                            inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), 
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                            )"""

                # create table if not exists
                self.cur.execute(prepared_stmt)
                self.conn.commit()
                print("Table '" + table_name + "' created successfully!")
            except psycopg2.Error as e:
                print("Error creating table:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def create_trigger(self, table_name):
        if self.cur:
            try:
                prepared_stmt = None
                if table_name == "user_message_inbox_duplicate":
                    prepared_stmt = """CREATE OR REPLACE TRIGGER set_timestamp 
                            BEFORE UPDATE ON user_message_inbox_duplicate
                            FOR EACH ROW 
                            EXECUTE PROCEDURE trigger_set_timestamp()"""
                elif table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = """CREATE OR REPLACE TRIGGER set_timestamp 
                        BEFORE UPDATE ON user_message_inbox_perceptually_similar 
                        FOR EACH ROW 
                        EXECUTE PROCEDURE trigger_set_timestamp()"""

                # create trigger
                self.cur.execute(prepared_stmt)
                self.conn.commit()
                print("Trigger for '" + table_name + "' created successfully!")
            except psycopg2.Error as e:
                print("Error creating trigger:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def store(self, value_column_value, worker_column_value):
        if self.cur:
            try:
                prepared_stmt = None
                if self.table_name == "user_message_inbox_duplicate":
                    prepared_stmt = "INSERT INTO user_message_inbox_duplicate (value, worker_name) VALUES (%s, %s)"
                elif self.table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = "INSERT INTO user_message_inbox_perceptually_similar (value, worker_name) VALUES (%s, %s)"

                self.cur.execute(
                    prepared_stmt,
                    (value_column_value, worker_column_value),
                )
                self.conn.commit()
                print("Value stored successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error storing value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def update(self, table_name, id_value, value_column_new_value, worker_column_new_value):
        if self.cur:
            try:
                prepared_stmt = None
                if table_name == "user_message_inbox_duplicate":
                    prepared_stmt = "UPDATE user_message_inbox_duplicate SET value = %s, worker_name = %s WHERE id = %s"
                elif table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = "UPDATE user_message_inbox_perceptually_similar SET value = %s, worker_name = %s WHERE id = %s"

                self.cur.execute(
                    prepared_stmt,
                    (value_column_new_value, worker_column_new_value, id_value),
                )
                self.conn.commit()
                print("Value updated successfully at " + table_name + "!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error updating value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def delete(self, table_name, id_value):
        if self.cur:
            try:
                prepared_stmt = None
                if table_name == "user_message_inbox_duplicate":
                    prepared_stmt = "DELETE FROM user_message_inbox_duplicate WHERE id = %s"
                elif table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = "DELETE FROM user_message_inbox_perceptually_similar WHERE id = %s"

                self.cur.execute(
                    prepared_stmt,
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
                prepared_stmt = None
                if table_name == "user_message_inbox_duplicate":
                    prepared_stmt = "DROP TABLE IF EXISTS user_message_inbox_duplicate"
                elif table_name == "user_message_inbox_perceptually_similar":
                    prepared_stmt = "DROP TABLE IF EXISTS user_message_inbox_perceptually_similar"

                self.cur.execute(prepared_stmt)
                self.conn.commit()
                print("Table '" + table_name + "' deleted successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error deleting table:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def initialise(self):
        self.create_trigger_function()
        self.create_table(self.table_name)
        self.create_trigger(self.table_name)