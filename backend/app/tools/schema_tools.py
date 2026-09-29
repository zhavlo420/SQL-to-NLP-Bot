from sqlalchemy import inspect
from app.db import engine

def get_schema():
    inspector = inspect(engine)
    output = []
    for table in inspector.get_table_names():
        output.append({
            "table": table,
            "columns": [
                {"name": c["name"], "type": str(c["type"]), "nullable": c["nullable"]}
                for c in inspector.get_columns(table)
            ],
            "primary_key": inspector.get_pk_constraint(table).get("constrained_columns", []),
            "foreign_keys": inspector.get_foreign_keys(table)
        })
    return output
