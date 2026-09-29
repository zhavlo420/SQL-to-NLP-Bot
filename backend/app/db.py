from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

def execute_sql(sql: str):
    with engine.begin() as conn:
        result = conn.execute(text(sql))
        rows = [dict(r._mapping) for r in result.fetchmany(settings.max_result_rows)]
        return {"columns": list(result.keys()), "rows": rows, "row_count": len(rows)}
