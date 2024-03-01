import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
class Postgres:
    def __init__(self):
        self.connection = None

    """
    Connect to postgres database
    """
    def connect(self):
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=int(os.getenv('POSTGRES_PORT')),
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )

    """
    List all tables in the database
    """
    def list_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)

        tables = cursor.fetchall()
        cursor.close()

        return tables

    """
    Get table information
    """
    def get_table_info(self,table_name):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s and table_schema = 'public';
        """, (table_name,))

        table_info = cursor.fetchall()
        cursor.close()

        return table_info

    """
    Get data from database
    """
    def get_data(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return data