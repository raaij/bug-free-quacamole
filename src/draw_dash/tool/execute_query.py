import duckdb
from .diagnose_sql_error import diagnose_sql_error, format_diagnosis_for_agent


def execute_query(query: str):
    """
    Executes a query against the database with enhanced error handling and diagnosis.

    Args:
        query (str): The query to execute.
        
    Returns:
        pandas.DataFrame or str: Query results as dataframe or detailed error diagnosis
    """
    try:
        result = duckdb.sql(query)
    except duckdb.Error as error:
        # Generate detailed diagnosis for the error
        diagnosis = diagnose_sql_error(query, str(error))
        formatted_diagnosis = format_diagnosis_for_agent(diagnosis)
        
        return f"QUERY EXECUTION FAILED:\n{formatted_diagnosis}"

    if result is None:
        return "Query executed successfully with no results."

    # Convert dataframe to JSON string for serialization
    df = result.df()
    return df.to_json(orient='records')