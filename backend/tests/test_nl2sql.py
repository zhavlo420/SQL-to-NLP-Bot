from app.agents.sql_agent import generate_sql


def test_top_products_revenue_query():
    sql = generate_sql("Top 5 products by revenue", [])
    assert "SELECT" in sql.upper()
    assert "SUM(o.total_amount)" in sql
    assert "ORDER BY REVENUE DESC" in sql.upper()
    assert "LIMIT 5" in sql.upper()


def test_customer_count_query():
    sql = generate_sql("How many customers are there?", [])
    assert "COUNT(*)" in sql.upper()
    assert "FROM CUSTOMERS" in sql.upper()
