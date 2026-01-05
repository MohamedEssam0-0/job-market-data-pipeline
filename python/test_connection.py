from db_connection import get_connection

print("🚀 Starting connection test")

conn = get_connection()

if conn:
    conn.close()
    print("🔌 Connection closed successfully")
