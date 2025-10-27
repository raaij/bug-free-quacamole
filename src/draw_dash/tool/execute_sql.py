import duckdb

def execute_sql(query: str) -> str:
    """
    Executes a query against the database.

    Args:
        query (str): The query to execute.
    """
    try:
        result = duckdb.sql(query)
    except duckdb.Error as error:
        return "An error occurred: {}".format(error)

    if result is None:
        return "Query executed successfully with no results."

    return result.df().to_markdown(index=True)
