from draw_dash.tool import execute_query


def test_execute_query():
    result = execute_query("""
SELECT CUST_ID, BALANCE
FROM marketing
LIMIT 10
""")

    assert "CUST_ID" in result
    assert "BALANCE" in result
