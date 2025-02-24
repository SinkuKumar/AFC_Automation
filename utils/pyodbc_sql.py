"""
PyODBC SQL

This module contains the PyODBCSQL class, which allows executing SQL queries and performing data operations on a MS SQL database.

:module: pyodbc_sql.py
:platform: Unix, Windows
:synopsis: Executes SQL queries and performing data operations with a SQL database.

:date: Feb 24, 2025
:author: Sinku Kumar `sinkukumar.r@hq.graphxsys.com <mailto:sinkukumar.r@hq.graphxsys.com>`_
"""

# TODO: Implement logging along with proper error handling with error codes, as per guidelines.

import os
import pyodbc

# TODO: Remove this in production.
from dotenv import load_dotenv
load_dotenv("./utils/.env")


class PyODBCSQL:
    """
    A class for executing SQL queries and performing data operations with a SQL database.

    :Attributes:
        server: The name of the SQL server.
        database: The name of the database.
        username: The username for the SQL server.
        password: The password for the SQL server.
        conn: The connection to the SQL server.

    :Methods:
        :execute_query(self, query: str) -> Any: Executes the specified SQL query and returns the result.
        :get_column_names(self, table_name: str) -> list[tuple[str, str]]: Returns the column names of the specified table.
        :delete_table_data(self, table_name: str) -> None: Deletes the data from the specified table.
        :insert_csv_data(self, table_name: str, csv_file_path: str) -> None:
        :bulk_insert_csv_sql(self, file_path: str, staging_table_name: str, client_id: str) -> None:
    """

    def __init__(self):
        """
        Initializes the MSSQLDatabase class.

        :return: None
        :rtype: None
        """
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.conn = None

    def execute_query(self, query: str) -> list[tuple[str, str]]:
        """
        Executes a SQL query and returns the result.

        :param query: The SQL query to execute.
        :type query: str

        :return: The result of the query.
        :rtype: list[tuple[str, str]] | None
        """

        self.conn = pyodbc.connect(
            f"""DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};
                                UID={self.username};PWD={self.password}""",
            TrustServerCertificate="yes",
        )
        
      
        cursor = self.conn.cursor()
        cursor.execute(query)

        if cursor.description is not None:
            data = cursor.fetchall()
        else:
            data = None

        self.conn.commit()
        cursor.close()
        self.conn.close()
        return data

    def get_column_names(self, table_name: str) -> list[tuple[str, str]]:
        """
        Returns the column names of the specified table.

        :param table_name: The name of the table to get the column names from.
        :type table_name: str

        :return: The column names of the specified table.
        :rtype: list[tuple[str, str]]
        """
        column_names_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
        return self.execute_query(column_names_query)

if __name__ == "__main__":
    sql = PyODBCSQL()
    result = sql.execute_query("SELECT 'Result' AS Test")
    print(result)
