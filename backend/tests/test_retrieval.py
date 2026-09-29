from app.agents.glossary_agent import canonicalize_question, retrieve_glossary
from app.agents.schema_agent import select_relevant_schema
from app.agents.sql_agent import generate_sql


def test_glossary_retrieves_business_synonyms():
    glossary = retrieve_glossary("sales by location")

    assert {entry["term"] for entry in glossary} >= {"revenue", "city"}


def test_schema_retrieval_uses_glossary_references():
    glossary = retrieve_glossary("sales by location")
    schema = [
        {"table": "orders", "columns": [{"name": "total_amount"}]},
        {"table": "customers", "columns": [{"name": "city"}]},
        {"table": "inventory", "columns": [{"name": "stock_count"}]},
    ]

    relevant = select_relevant_schema("sales by location", schema, glossary)

    assert [table["table"] for table in relevant] == ["orders", "customers"]


def test_glossary_terms_canonicalize_for_sql_generation():
    glossary = retrieve_glossary("sales by location")

    assert "revenue by city" in canonicalize_question("sales by location", glossary)
    sql = generate_sql("sales by location", [], glossary)
    assert "SUM(o.total_amount)" in sql
    assert "c.city" in sql


def test_canonical_customer_count_keeps_customer_query_template():
    glossary = retrieve_glossary("How many customers are there?")

    sql = generate_sql("How many customers are there?", [], glossary)

    assert "COUNT(*)" in sql
    assert "FROM customers" in sql