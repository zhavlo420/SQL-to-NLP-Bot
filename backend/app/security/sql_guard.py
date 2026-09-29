import sqlglot
from sqlglot import exp

FORBIDDEN = {
    exp.Insert: "INSERT",
    exp.Update: "UPDATE",
    exp.Delete: "DELETE",
    exp.Drop: "DROP",
    exp.Alter: "ALTER",
    exp.TruncateTable: "TRUNCATE",
    exp.Create: "CREATE",
    exp.Merge: "MERGE",
}

def validate_sql(sql: str) -> dict:
    try:
        statements = sqlglot.parse(sql, read="postgres")
    except Exception as exc:
        return {"allowed": False, "reason": f"SQL parse error: {exc}"}

    if len(statements) != 1:
        return {"allowed": False, "reason": "Only one SQL statement is permitted."}

    tree = statements[0]
    if not isinstance(tree, (exp.Select, exp.Union)):
        return {"allowed": False, "reason": "Only SELECT queries are permitted."}

    for node in tree.walk():
        operation = FORBIDDEN.get(type(node))
        if operation:
            return {"allowed": False, "reason": f"Forbidden SQL operation: {operation}"}

    return {"allowed": True, "reason": "Read-only SQL policy passed."}
