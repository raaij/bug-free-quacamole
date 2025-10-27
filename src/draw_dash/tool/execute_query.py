import duckdb


def execute_query(query: str):
    """
    Executes a query against the database.

    Args:
        query (str): The query to execute.
    """

    return duckdb.sql(query).df().to_markdown(index=True)
