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

    def create_trigger_function(self):
        if self.cur:
            try:
                # create trigger function
                self.cur.execute(
                    """CREATE OR REPLACE FUNCTION trigger_set_timestamp()
                        RETURNS TRIGGER AS $$
                        BEGIN
                          NEW.updated_at = NOW();
                          RETURN NEW;
                        END;
                        $$ LANGUAGE plpgsql"""
                )
                self.conn.commit()
                print("Trigger function created successfully!")
            except psycopg2.Error as e:
                print("Error creating trigger function:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def create_table(self, table_name, value_column, worker_column):
        if self.cur:
            try:
                if table_name == "user_message_inbox_duplicate":
                    self.cur.execute(
                        f"""CREATE TABLE IF NOT EXISTS {table_name} (
                            id SERIAL PRIMARY KEY,
                            {value_column} VARCHAR(128),
                            {worker_column} VARCHAR(128),
                            inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                            )"""
                    )
                    self.conn.commit()
                    print(f"Table '{table_name}' created successfully!")
                elif table_name == "user_message_inbox_perceptually_similar":
                    # create table if not exists
                    self.cur.execute(
                        f"""CREATE TABLE IF NOT EXISTS {table_name} (
                            id SERIAL NOT NULL PRIMARY KEY, 
                            {value_column} VARCHAR(128), 
                            {worker_column} VARCHAR(128), 
                            inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), 
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                            )"""
                    )
                    self.conn.commit()
                    print(f"Table '{table_name}' created successfully!")
            except psycopg2.Error as e:
                print("Error creating table:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def create_trigger(self, table_name):
        if self.cur:
            try:
                # create trigger
                self.cur.execute(
                    f"""CREATE OR REPLACE TRIGGER set_timestamp 
                        BEFORE UPDATE ON {table_name} 
                        FOR EACH ROW 
                        EXECUTE PROCEDURE trigger_set_timestamp()"""
                )
                self.conn.commit()
                print(f"Trigger for '{table_name}' created successfully!")
            except psycopg2.Error as e:
                print("Error creating trigger:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def store(self, table_name, value_column, value_column_value, worker_column, worker_column_value):
        if self.cur:
            try:
                if table_name == "user_message_inbox_duplicate":
                    self.cur.execute(
                        f"""INSERT INTO {table_name} ({value_column}, {worker_column}) VALUES (%s, %s)""",
                        (value_column_value, worker_column_value),
                    )
                    self.conn.commit()
                    print("Value stored successfully!")
                elif table_name == "user_message_inbox_perceptually_similar":
                    self.cur.execute(
                        "INSERT INTO %s (%s, %s) VALUES (%s, %s)",
                        (table_name, value_column, worker_column, value_column_value, worker_column_value),
                    )
                    self.conn.commit()
                    print(f"Value stored successfully in {table_name}!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error storing value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def update(self, table_name, value_column, id_value, value_column_new_value, worker_column, worker_column_new_value):
        if self.cur:
            try:
                if table_name == "user_message_inbox_duplicate":
                    self.cur.execute(
                    f"""UPDATE {table_name} SET {value_column} = %s, {worker_column} = %s WHERE id = %s""",
                    (value_column_new_value, worker_column_new_value, id_value),
                    )
                    self.conn.commit()
                    print(f"Value updated successfully at {table_name}!")
                    pass
                elif table_name == "user_message_inbox_perceptually_similar":
                    self.cur.execute(
                        "UPDATE %s SET %s = %s, %s = %s WHERE id = %s",
                        (table_name, value_column, value_column_new_value,
                         worker_column, worker_column_new_value, id_value),
                    )
                    self.conn.commit()
                    print(f"Value updated successfully in {table_name}!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print("Error updating value:", e)
        else:
            print("Not connected to the database. Call connect() first.")

    def delete(self, table_name, column_name, id_value):
        if self.cur:
            try:
                self.cur.execute(
                    "DELETE FROM %s WHERE %s = %s",
                    (table_name, column_name, id_value,),
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
#     pg_manager.create_trigger_function()
#     pg_manager.create_table("user_message_inbox_duplicate", "value", "hash_worker")
#     pg_manager.create_trigger("user_message_inbox_duplicate")
#     pg_manager.update("user_message_inbox_duplicate", "value", 1, "some_new_hash", "worker_name", "blake2b_hash_value")
#     pg_manager.close_connection()