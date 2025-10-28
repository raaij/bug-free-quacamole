import os

import duckdb
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import json

from draw_dash.db import PATH_DATA

# Global database connection
_connection: Optional[duckdb.DuckDBPyConnection] = None

def read_data_files():
    return [
        str(PATH_DATA.resolve() / file)
        for file in os.listdir(PATH_DATA)
    ]


def connect_to_db(db_path: Optional[str] = None) -> None:
    """
    Initialize the DuckDB connection.

    Args:
        db_path: Path to the DuckDB database file. If None, uses an in-memory database.
    """
    global _connection
    if _connection:
        _connection.close()  # Close existing connection if any
    _connection = duckdb.connect(db_path or ":memory:")

connect_to_db()

def close_db_connection() -> None:
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None


def ingest_file(file_path: str, table_name: str = "dataset") -> Dict[str, Any]:
    """
    Ingest a file into DuckDB.

    Args:
        file_path: Path to the file (CSV, JSON, or Parquet).
        table_name: Name for the table in DuckDB.

    Returns:
        Metadata dictionary with schema, row count, etc.
    """
    if not _connection:
        raise ConnectionError("Database connection is not initialized. Call connect_to_db() first.")

    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path_obj}")

    suffix = file_path_obj.suffix.lower()
    try:
        if suffix == ".csv":
            _connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')")
        elif suffix == ".json":
            _connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_json_auto('{file_path}')")
        elif suffix == ".parquet":
            _connection.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}')")
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        return get_table_metadata(table_name)
    except Exception as e:
        raise Exception(f"Failed to ingest file: {e}")


def get_table_metadata(table_name: str = "dataset") -> Dict[str, Any]:
    """
    Extract metadata from a table.

    Args:
        table_name: Name of the table.

    Returns:
        Dictionary with metadata.
    """
    if not _connection:
        raise ConnectionError("Database connection is not initialized. Call connect_to_db() first.")

    try:
        row_count = _connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        schema_info = _connection.execute(f"DESCRIBE {table_name}").fetchall()

        columns = [{"name": col[0], "type": col[1], "null": col[2] if len(col) > 2 else "YES"} for col in schema_info]

        column_stats = {}
        for col in columns:
            col_name, col_type = col["name"], col["type"].upper()

            try:
                if any(t in col_type for t in ["INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC"]):
                    stats = _connection.execute(
                        f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}), COUNT(DISTINCT {col_name}) FROM {table_name}").fetchone()
                    column_stats[col_name] = {
                        "min": float(stats[0]) if stats[0] is not None else None,
                        "max": float(stats[1]) if stats[1] is not None else None,
                        "avg": float(stats[2]) if stats[2] is not None else None,
                        "distinct_count": int(stats[3]) if stats[3] is not None else None
                    }
                elif "VARCHAR" in col_type or "TEXT" in col_type:
                    distinct_count = \
                    _connection.execute(f"SELECT COUNT(DISTINCT {col_name}) FROM {table_name}").fetchone()[0]
                    column_stats[col_name] = {"distinct_count": int(distinct_count)}
            except Exception:
                pass  # Skip if stats extraction fails

        sample_data = _connection.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf().to_dict('records')
        import json

        return json.dumps({
            "table_name": table_name,
            "row_count": row_count,
            "column_count": len(columns),
            "columns": columns,
            "column_stats": column_stats,
            "sample_data": sample_data,
        })
    except Exception as e:
        raise Exception(f"Failed to extract metadata: {e}")


def execute_query(query: str) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a DataFrame.

    Args:
        query: SQL query string.

    Returns:
        Pandas DataFrame with results.
    """
    if not _connection:
        raise ConnectionError("Database connection is not initialized. Call connect_to_db() first.")

    try:
        return _connection.execute(query).fetchdf().head(50).to_markdown()
    except Exception as e:
        raise Exception(f"Query execution failed: {e}")


def get_table_list() -> list:
    """
    Get a list of all tables in the database.

    Returns:
        List of table names.
    """
    if not _connection:
        raise ConnectionError("Database connection is not initialized. Call connect_to_db() first.")

    tables = _connection.execute("SHOW TABLES").fetchall()
    return [table[0] for table in tables]


def drop_table(table_name: str) -> None:
    """
    Drop a table from the database.

    Args:
        table_name: Name of the table to drop.
    """
    if not _connection:
        raise ConnectionError("Database connection is not initialized. Call connect_to_db() first.")

    try:
        _connection.execute(f"DROP TABLE IF EXISTS {table_name}")
    except Exception as e:
        raise Exception(f"Failed to drop table: {e}")
