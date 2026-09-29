from app.agents.glossary_agent import canonicalize_question


def generate_sql(
    question: str,
    schema: list[dict],
    glossary: list[dict] | None = None,
) -> str:
    q = canonicalize_question(question, glossary or []).lower()

    if "top 5" in q and "product" in q and ("revenue" in q or "sales" in q):
        return """SELECT p.name AS product,
       SUM(o.total_amount) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.name
ORDER BY revenue DESC
LIMIT 5"""

    if any(phrase in q for phrase in ("how many customers", "number of customers", "customer count")):
        return "SELECT COUNT(*) AS customer_count FROM customers"

    if "revenue" in q and "city" in q:
        return """SELECT c.city, SUM(o.total_amount) AS revenue
FROM orders o
JOIN customers c ON c.id = o.customer_id
GROUP BY c.city
ORDER BY revenue DESC"""

    # Safe demo fallback. Replace with structured-output LLM generation.
    return "SELECT COUNT(*) AS total_orders FROM orders"
