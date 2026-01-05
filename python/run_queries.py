import os
from db_connection import get_connection

SQL_FOLDER = "../project_sql"

def read_sql_file(filepath):
    with open(filepath, "r") as file:
        return file.read()

def run_query(sql_query):
    conn = get_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print("❌ Query failed:")
        print(e)
        return None
    finally:
        conn.close()

def main():
    sql_files = sorted([
        f for f in os.listdir(SQL_FOLDER)
        if f.endswith(".sql")
    ])

    for file in sql_files:
        print("\n" + "="*60)
        print(f"▶ Running query: {file}")
        print("="*60)

        sql_path = os.path.join(SQL_FOLDER, file)
        query = read_sql_file(sql_path)
        results = run_query(query)

        if results:
            print(f"✅ Rows returned: {len(results)}")
            print("🔹 Sample rows:")
            for row in results[:5]:
                print(row)
        else:
            print("⚠️ No results or query failed")

if __name__ == "__main__":
    main()
