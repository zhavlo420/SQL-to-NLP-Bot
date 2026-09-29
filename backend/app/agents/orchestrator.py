from app.agents.intent_agent import classify_intent
from app.agents.glossary_agent import retrieve_glossary
from app.agents.schema_agent import retrieve_schema
from app.agents.planner_agent import make_plan
from app.agents.sql_agent import generate_sql
from app.agents.reviewer_agent import review_sql
from app.agents.result_agent import analyze_result
from app.tools.sql_tools import execute_safe_sql

def run_agent(question: str):
    trace = []
    def event(agent, message):
        trace.append({"agent": agent, "message": message})

    event("Orchestrator", "Understanding the request")
    intent = classify_intent(question)

    event("Glossary Agent", "Retrieving business definitions")
    glossary = retrieve_glossary(question)

    event("Schema Agent", "Retrieving relevant database metadata")
    schema = retrieve_schema(question, glossary)

    event("Planner Agent", "Creating a query plan")
    plan = make_plan(question, intent, schema, glossary)

    review = {"allowed": False, "reason": "not reviewed"}
    retry = 0
    while retry < 3:
        event("SQL Generator", f"Generating SQL (attempt {retry + 1})")
        sql = generate_sql(question, schema, glossary)
        event("SQL Reviewer", "Validating SQL syntax and policy")
        review = review_sql(sql)
        if review["allowed"]:
            break
        retry += 1
        event("Repair", f"SQL rejected: {review['reason']}")

    if not review["allowed"]:
        raise ValueError(f"SQL rejected after retries: {review['reason']}")

    event("Executor", "Executing read-only query")
    result = execute_safe_sql(sql)

    event("Result Analyst", "Analyzing returned data")
    analysis = analyze_result(question, result)

    return {
        "answer": analysis["summary"],
        "sql": sql,
        "rows": result["rows"],
        "columns": result["columns"],
        "trace": trace,
        "assumptions": [
            "The demo defines revenue as orders.total_amount.",
            "Only read-only SQL is permitted."
        ]
    }
