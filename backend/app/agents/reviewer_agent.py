from app.security.sql_guard import validate_sql

def review_sql(sql: str) -> dict:
    return validate_sql(sql)
