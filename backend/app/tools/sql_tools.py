from app.security.sql_guard import validate_sql
from app.db import execute_sql

def execute_safe_sql(sql: str):
    policy = validate_sql(sql)
    if not policy["allowed"]:
        raise ValueError(policy["reason"])
    return execute_sql(sql)
