from app.security.sql_guard import validate_sql

def test_select_allowed():
    assert validate_sql("SELECT * FROM customers")["allowed"]

def test_select_with_forbidden_words_in_string_allowed():
    assert validate_sql("SELECT 'update and drop' AS note")["allowed"]

def test_delete_blocked():
    assert not validate_sql("DELETE FROM customers")["allowed"]

def test_write_in_cte_blocked():
    sql = "WITH removed AS (DELETE FROM customers RETURNING *) SELECT * FROM removed"
    assert not validate_sql(sql)["allowed"]

def test_drop_blocked():
    assert not validate_sql("DROP TABLE customers")["allowed"]
