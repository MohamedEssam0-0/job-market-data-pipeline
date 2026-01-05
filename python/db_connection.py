import psycopg2
from db_config import DB_CONFIG

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to PostgreSQL (sql_course)")
        return conn
    except Exception as e:
        print("❌ Failed to connect to PostgreSQL")
        print(e)
        return None
