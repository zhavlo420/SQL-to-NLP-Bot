import re
from collections import defaultdict


def select_relevant_schema(
    question: str,
    schema: list[dict],
    glossary: list[dict] | None = None,
    max_tables: int = 4,
) -> list[dict]:
    if not schema:
        return schema

    query_tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
    scores = defaultdict(int)
    table_names = {table["table"] for table in schema}

    for table in schema:
        name = table["table"]
        schema_tokens = set(re.findall(r"[a-z0-9]+", name.lower()))
        for column in table.get("columns", []):
            schema_tokens.update(re.findall(r"[a-z0-9]+", column["name"].lower()))
        scores[name] += 2 * len(query_tokens & schema_tokens)

    for entry in glossary or []:
        for table in entry.get("tables", []):
            if table in table_names:
                scores[table] += 4

    relevant = [table for table in schema if scores[table["table"]] > 0]
    if not relevant:
        return schema

    ranked = sorted(
        relevant,
        key=lambda table: (-scores[table["table"]], schema.index(table)),
    )[:max_tables]
    selected_names = {table["table"] for table in ranked}
    return [table for table in schema if table["table"] in selected_names]


def retrieve_schema(question: str, glossary: list[dict] | None = None) -> list[dict]:
    from app.tools.schema_tools import get_schema

    return select_relevant_schema(question, get_schema(), glossary)
