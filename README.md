# 📊 Job Market Data Engineering Pipeline (PostgreSQL + Python)

## 📌 Overview

This project is a **data engineering pipeline** that automates the execution of analytical SQL queries on a PostgreSQL database using Python.

The pipeline is designed to:

- Connect to a relational database  
- Execute multiple SQL files programmatically  
- Orchestrate queries in a reproducible way  
- Export results into structured formats for downstream analysis  

This project focuses on **engineering, orchestration, and automation**, rather than pure analysis.

---

## 🎯 Project Objectives

- Build a reusable **Python–PostgreSQL integration**
- Automate execution of multiple SQL analysis queries
- Separate configuration, connection logic, and execution logic
- Demonstrate real-world **data engineering best practices**
- Produce clean, reproducible outputs from raw database tables

## 🏗️ Architecture Overview

PostgreSQL Database
↓
SQL files (.sql)
↓
Python Orchestration Layer
↓
Structured Outputs (CSV)


### Key Design Principles

- Separation of concerns  
- Reusable database connections  
- Configurable and scalable pipeline  
- Safe handling of large datasets (not committed to Git)

---

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|------------|
| Database         | PostgreSQL |
| Language         | Python 3 |
| SQL              | Advanced SQL (CTEs, joins, aggregations) |
| DB Connector     | psycopg2 |
| Version Control  | Git & GitHub |
| Environment      | Python virtual environment (venv) |

---

## 📂 Project Structure

```text
job-market-data-pipeline/
├── python/
│   ├── db_config.py           # Database configuration (local only)
│   ├── db_connection.py       # Reusable PostgreSQL connection logic
│   ├── run_queries.py         # Executes SQL files dynamically
│   ├── export_to_csv.py       # Exports query results to CSV
│   ├── test_connection.py     # Connection sanity check
│   └── analyze_results.py     # Reserved for future transformations
│
├── README.md
└── .gitignore
```

---

## ⚙️ Pipeline Workflow

### 1️⃣ Database Connection
- PostgreSQL credentials are defined locally  
- Python establishes a secure connection using `psycopg2`

### 2️⃣ SQL Orchestration
- SQL queries are stored as standalone `.sql` files  
- Python dynamically reads and executes them  
- This allows easy query updates without changing Python logic  

### 3️⃣ Query Execution
- Queries are executed sequentially  
- Results are fetched with schema metadata (column names)

### 4️⃣ Output Generation
- Results are exported as CSV files (locally)  
- Large datasets are intentionally excluded from GitHub  

---

## 🧪 Scripts Explained

### `db_connection.py`
- Centralized database connection handler  
- Prevents duplicated connection logic  
- Implements safe connection opening and closing

```bash
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

``` 

------

### `run_queries.py`
- Reads all SQL files from a directory  
- Executes them programmatically  
- Prints row counts and sample results  
- Acts as the orchestration layer

```bash
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

```

-----

### `export_to_csv.py`
- Extends query execution  
- Extracts column names automatically  
- Saves structured CSV outputs for analysis

```bash
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

```

------

### `test_connection.py`
- Lightweight sanity check  
- Confirms PostgreSQL connectivity before running the pipeline  

```bash
from db_connection import get_connection

print("🚀 Starting connection test")

conn = get_connection()

if conn:
    conn.close()
    print("🔌 Connection closed successfully")

```

------

### `analyze_results.py`
- Placeholder for future transformations  
- Intended for:
  - Pandas analysis  
  - Feature engineering  
  - Business metrics computation
 
```bash
"""
analyze_results.py

This module is reserved for future data analysis and transformations.
Possible extensions:
- Aggregations using pandas
- Business KPIs computation
- Feature engineering for downstream analytics or ML
"""

```

---

## 🔐 Data & Security Handling

- Large datasets are **not committed** to GitHub  
- Raw tables are stored locally or in the database  
- Sensitive credentials are excluded via `.gitignore`  
- This follows real-world data engineering standards  

---

## 🚀 How to Run the Project Locally

### 1️⃣ Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies
```bash
pip install psycopg2-binary
```
### 3️⃣ Test Database Connection
```bash
python python/test_connection.py
```
### 4️⃣ Execute SQL Queries
```bash
python python/run_queries.py
```
### 5️⃣ Export Results to CSV
```bash
python python/export_to_csv.py
```

## 📈 What This Project Demonstrates

- Practical data engineering mindset  
- Python–PostgreSQL integration  
- Query orchestration and automation  
- Clean project structure and modular design  
- Safe handling of large datasets  
- Production-ready Git workflow  

---

## 💼 Use Case

This pipeline can be adapted for:

- Analytics engineering  
- ETL pipelines  
- Automated reporting  
- Data warehouse query orchestration  
- Preprocessing layers for machine learning  

---

## 🧭 Future Improvements

- Environment variables for configuration  
- Pandas-based transformation layer  
- Logging instead of print statements  
- Scheduling with Airflow or cron  
- Dockerization for deployment  



