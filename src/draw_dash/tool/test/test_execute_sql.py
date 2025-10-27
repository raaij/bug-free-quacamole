from draw_dash.tool import execute_sql


def test_execute_query():
    result = execute_sql("""
SELECT CUST_ID, BALANCE
FROM marketing
LIMIT 10
""")

    assert "CUST_ID" in result
    assert "BALANCE" in result


def test_execute_query_incorrect():
    result = execute_sql("abcdef")
    assert "error" in result


def test_execute_query_insert():
    result = execute_sql("CREATE TABLE newtable (id INTEGER, name VARCHAR);")
    assert "success" in result
