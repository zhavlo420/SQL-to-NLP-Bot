from app.db import execute_sql

if __name__ == "__main__":
    print(execute_sql("SELECT COUNT(*) AS customers FROM customers"))
