import duckdb
import re
from typing import Dict, Any


def diagnose_sql_error(query: str, error_message: str) -> Dict[str, Any]:
    """
    Diagnoses SQL execution errors and provides detailed analysis for query correction.
    
    Args:
        query (str): The failed SQL query
        error_message (str): The error message from the database
        
    Returns:
        Dict containing error analysis and suggestions for fixing the query
    """
    diagnosis = {
        "error_type": "",
        "error_details": error_message,
        "suggestions": [],
        "schema_info": {},
        "corrected_query_hints": []
    }
    
    # Get current database schema information
    try:
        # Get all tables
        tables_result = duckdb.sql("SHOW TABLES").fetchall()
        available_tables = [table[0] for table in tables_result]
        diagnosis["schema_info"]["available_tables"] = available_tables
        
        # Get column information for each table
        for table in available_tables:
            try:
                columns_result = duckdb.sql(f"DESCRIBE {table}").fetchall()
                diagnosis["schema_info"][table] = {
                    "columns": [{"name": col[0], "type": col[1]} for col in columns_result]
                }
            except Exception:
                continue
                
    except Exception as e:
        diagnosis["schema_info"]["error"] = f"Could not retrieve schema: {str(e)}"
    
    # Analyze error types and provide specific suggestions
    error_lower = error_message.lower()
    
    # Table/Column not found errors
    if "table" in error_lower and ("not found" in error_lower or "does not exist" in error_lower):
        diagnosis["error_type"] = "table_not_found"
        
        # Extract table name from query
        table_matches = re.findall(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
        table_matches.extend(re.findall(r'\bJOIN\s+(\w+)', query, re.IGNORECASE))
        
        diagnosis["suggestions"].extend([
            f"Table not found. Available tables: {', '.join(available_tables)}",
            "Check table name spelling and case sensitivity",
            "Ensure the table exists in the current database"
        ])
        
        if table_matches:
            diagnosis["corrected_query_hints"].append(
                f"Replace table name '{table_matches[0]}' with one of: {', '.join(available_tables)}"
            )
    
    elif "column" in error_lower and ("not found" in error_lower or "does not exist" in error_lower):
        diagnosis["error_type"] = "column_not_found"
        
        # Extract column references from error message
        column_match = re.search(r"column['\"]?\s*([^'\"]*)['\"]?", error_message, re.IGNORECASE)
        if column_match:
            missing_column = column_match.group(1).strip()
            diagnosis["suggestions"].extend([
                f"Column '{missing_column}' not found",
                "Check column name spelling and case sensitivity",
                "Verify the column exists in the specified table"
            ])
            
            # Suggest similar column names
            for table, info in diagnosis["schema_info"].items():
                if isinstance(info, dict) and "columns" in info:
                    similar_columns = [
                        col["name"] for col in info["columns"] 
                        if missing_column.lower() in col["name"].lower() or 
                           col["name"].lower() in missing_column.lower()
                    ]
                    if similar_columns:
                        diagnosis["corrected_query_hints"].append(
                            f"In table '{table}', similar columns: {', '.join(similar_columns)}"
                        )
    
    # Syntax errors
    elif "syntax error" in error_lower or "parser error" in error_lower:
        diagnosis["error_type"] = "syntax_error"
        diagnosis["suggestions"].extend([
            "SQL syntax error detected",
            "Check for missing commas, parentheses, or quotes",
            "Verify SQL keyword spelling and structure",
            "Ensure proper use of SQL operators and functions"
        ])
        
        # Common syntax fixes
        if "unexpected" in error_lower:
            diagnosis["corrected_query_hints"].append(
                "Check for unexpected characters or keywords in the query"
            )
    
    # Data type errors
    elif "type" in error_lower and ("mismatch" in error_lower or "conversion" in error_lower):
        diagnosis["error_type"] = "type_error"
        diagnosis["suggestions"].extend([
            "Data type mismatch or conversion error",
            "Check data types in WHERE clauses and comparisons",
            "Ensure proper casting of data types",
            "Verify numeric operations are performed on numeric columns"
        ])
    
    # Aggregation errors
    elif "aggregate" in error_lower or "group by" in error_lower:
        diagnosis["error_type"] = "aggregation_error"
        diagnosis["suggestions"].extend([
            "Aggregation or GROUP BY error",
            "Ensure all non-aggregate columns are included in GROUP BY",
            "Check that aggregate functions are used correctly",
            "Verify HAVING clause references only aggregated columns"
        ])
    
    # Permission/access errors
    elif "permission" in error_lower or "access" in error_lower:
        diagnosis["error_type"] = "permission_error"
        diagnosis["suggestions"].extend([
            "Database access or permission error",
            "Check database connection and credentials",
            "Verify user has necessary permissions for the operation"
        ])
    
    # Generic error handling
    else:
        diagnosis["error_type"] = "unknown_error"
        diagnosis["suggestions"].extend([
            "Unknown error type",
            "Review the complete error message for specific details",
            "Check query syntax and table/column references",
            "Verify data types and constraints"
        ])
    
    # Add general debugging suggestions
    diagnosis["suggestions"].append("Consider simplifying the query to isolate the issue")
    diagnosis["suggestions"].append("Test individual parts of complex queries separately")
    
    return diagnosis


def format_diagnosis_for_agent(diagnosis: Dict[str, Any]) -> str:
    """
    Formats the diagnosis in a structured way for agent communication.
    
    Args:
        diagnosis: The diagnosis dictionary from diagnose_sql_error
        
    Returns:
        Formatted string for agent communication
    """
    formatted = f"""
SQL ERROR DIAGNOSIS:

Error Type: {diagnosis['error_type']}
Error Details: {diagnosis['error_details']}

AVAILABLE SCHEMA:
"""
    
    # Add schema information
    if "available_tables" in diagnosis["schema_info"]:
        formatted += f"Tables: {', '.join(diagnosis['schema_info']['available_tables'])}\n\n"
        
        for table, info in diagnosis["schema_info"].items():
            if isinstance(info, dict) and "columns" in info:
                formatted += f"Table '{table}' columns:\n"
                for col in info["columns"]:
                    formatted += f"  - {col['name']} ({col['type']})\n"
                formatted += "\n"
    
    # Add suggestions
    formatted += "SUGGESTIONS FOR FIXING:\n"
    for i, suggestion in enumerate(diagnosis["suggestions"], 1):
        formatted += f"{i}. {suggestion}\n"
    
    # Add specific correction hints
    if diagnosis["corrected_query_hints"]:
        formatted += "\nSPECIFIC CORRECTIONS:\n"
        for hint in diagnosis["corrected_query_hints"]:
            formatted += f"- {hint}\n"
    
    return formatted