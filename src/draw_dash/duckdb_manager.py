"""
DuckDB Manager for DrawDash
Handles database connections, data ingestion, and metadata extraction
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import json


class DuckDBManager:
    """Manager for DuckDB operations"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize DuckDB manager

        Args:
            db_path: Path to DuckDB database file. If None, uses in-memory database.
        """
        self.db_path = db_path
        self.connection = duckdb.connect(db_path or ":memory:")

    def ingest_file(
        self,
        file_path: str,
        table_name: str = "dataset"
    ) -> Dict[str, Any]:
        """
        Ingest a file into DuckDB

        Args:
            file_path: Path to the file (CSV, JSON, or Parquet)
            table_name: Name for the table in DuckDB

        Returns:
            Metadata dictionary with schema, row count, etc.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine file type and ingest
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".csv":
                # Ingest CSV
                self.connection.execute(
                    f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')"
                )

            elif suffix == ".json":
                # Ingest JSON
                self.connection.execute(
                    f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_json_auto('{file_path}')"
                )

            elif suffix == ".parquet":
                # Ingest Parquet
                self.connection.execute(
                    f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}')"
                )

            else:
                raise ValueError(f"Unsupported file type: {suffix}")

            # Extract metadata
            metadata = self.get_table_metadata(table_name)
            return metadata

        except Exception as e:
            raise Exception(f"Failed to ingest file: {str(e)}")

    def get_table_metadata(self, table_name: str = "dataset") -> Dict[str, Any]:
        """
        Extract metadata from a table

        Args:
            table_name: Name of the table

        Returns:
            Dictionary with metadata
        """
        try:
            # Get row count
            row_count = self.connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            # Get schema information
            schema_info = self.connection.execute(
                f"DESCRIBE {table_name}"
            ).fetchall()

            # Format schema
            columns = []
            for col in schema_info:
                columns.append({
                    "name": col[0],
                    "type": col[1],
                    "null": col[2] if len(col) > 2 else "YES"
                })

            # Get column statistics for numeric columns
            column_stats = {}
            for col in columns:
                col_name = col["name"]
                col_type = col["type"].upper()

                # Only get stats for numeric columns
                if any(t in col_type for t in ["INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC"]):
                    try:
                        stats = self.connection.execute(f"""
                            SELECT
                                MIN({col_name}) as min,
                                MAX({col_name}) as max,
                                AVG({col_name}) as avg,
                                COUNT(DISTINCT {col_name}) as distinct_count
                            FROM {table_name}
                        """).fetchone()

                        column_stats[col_name] = {
                            "min": float(stats[0]) if stats[0] is not None else None,
                            "max": float(stats[1]) if stats[1] is not None else None,
                            "avg": float(stats[2]) if stats[2] is not None else None,
                            "distinct_count": int(stats[3]) if stats[3] is not None else None
                        }
                    except:
                        # Skip if stats extraction fails
                        pass

                # For string/categorical columns, get distinct count
                elif "VARCHAR" in col_type or "TEXT" in col_type:
                    try:
                        distinct_count = self.connection.execute(f"""
                            SELECT COUNT(DISTINCT {col_name}) FROM {table_name}
                        """).fetchone()[0]

                        column_stats[col_name] = {
                            "distinct_count": int(distinct_count)
                        }
                    except:
                        pass

            # Get sample data (first 5 rows)
            sample_data = self.connection.execute(
                f"SELECT * FROM {table_name} LIMIT 5"
            ).fetchdf().to_dict('records')

            metadata = {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "columns": columns,
                "column_stats": column_stats,
                "sample_data": sample_data
            }

            return metadata

        except Exception as e:
            raise Exception(f"Failed to extract metadata: {str(e)}")

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame

        Args:
            query: SQL query string

        Returns:
            Pandas DataFrame with results
        """
        try:
            result = self.connection.execute(query).fetchdf()
            return result
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

    def get_table_list(self) -> list:
        """
        Get list of all tables in the database

        Returns:
            List of table names
        """
        tables = self.connection.execute("SHOW TABLES").fetchall()
        return [table[0] for table in tables]

    def drop_table(self, table_name: str):
        """
        Drop a table from the database

        Args:
            table_name: Name of the table to drop
        """
        try:
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        except Exception as e:
            raise Exception(f"Failed to drop table: {str(e)}")

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Global database manager instance
# Using in-memory database for now, can be changed to persistent file
db_manager = DuckDBManager()
