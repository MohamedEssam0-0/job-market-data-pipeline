import os
import csv
from db_connection import get_connection

SQL_FOLDER = "../project_sql"
OUTPUT_FOLDER = "../csv_files"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def read_sql_file(filepath):
    with open(filepath, "r") as file:
        return file.read()

def run_query_with_columns(sql_query):
    conn = get_connection()
    if not conn:
        return None, None

    try:
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return columns, rows
    except Exception as e:
        print("❌ Query failed:")
        print(e)
        return None, None
    finally:
        conn.close()

def export_csv(filename, columns, rows):
    path = os.path.join(OUTPUT_FOLDER, filename)

    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"📁 Exported: {path}")

def main():
    sql_files = sorted([
        f for f in os.listdir(SQL_FOLDER)
        if f.endswith(".sql")
    ])

    for file in sql_files:
        print(f"\n▶ Processing {file}")
        sql_path = os.path.join(SQL_FOLDER, file)
        query = read_sql_file(sql_path)

        columns, rows = run_query_with_columns(query)

        if rows:
            csv_name = file.replace(".sql", ".csv")
            export_csv(csv_name, columns, rows)
        else:
            print("⚠️ No data to export")

if __name__ == "__main__":
    main()
