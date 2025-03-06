"""
PyODBC SQL

This module contains the PyODBCSQL class, which allows executing SQL queries and performing data operations on a MS SQL database.

:module: pyodbc_sql.py
:platform: Unix, Windows
:synopsis: Executes SQL queries and performing data operations with a SQL database.

:date: Feb 24, 2025
:author: Sinku Kumar `sinkukumar.r@hq.graphxsys.com <mailto:sinkukumar.r@hq.graphxsys.com>`
"""

# TODO: Implement logging along with proper error handling with error codes, as per guidelines.

import os
import pyodbc


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

    def __init__(self, server, database, username, password):
        """
        Initializes the MSSQLDatabase class.

        :param server: MS-SQL host address.
        :type server: str
        :param database: The name of the database.
        :type database: str
        :param username: The username for the SQL server.
        :type username: str
        :param password: The password for the SQL server.
        :type password: str

        :return: None
        :rtype: None
        """
        self.server = server # os.getenv("SQL_SERVER")
        self.database = database # os.getenv("SQL_DATABASE")
        self.username = username # os.getenv("SQL_USERNAME")
        self.password = password# os.getenv("SQL_PASSWORD")
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
    
    def bulk_insert_data(self, file_type, csv_file_path, table_name):
        """
        Bulk insert data from a CSV file into a SQL table.

        :param file_type: The type of file to insert.
        :type file_type: str
        :param csv_file_path: The path to the CSV file.
        :type csv_file_path: str
        :param table_name: The name of the SQL table.
        :type table_name: str
        """
        query = f"""
        BULK INSERT {table_name}
        FROM '{csv_file_path}'
        WITH
        (
            FORMAT = '{file_type}',
            FIELDTERMINATOR = ',',
            ROWTERMINATOR = '\\n',
            FIRSTROW = 2,
            TABLOCK
        );
        """
        self.execute_query(query)

    def delete_table_data(self, table_name: str) -> None:
        """
        Deletes the data from the specified table.

        :param table_name: The name of the table to delete the data from.
        :type table_name: str
        """
        delete_query = f"TRUNCATE TABLE {table_name};"
        self.execute_query(delete_query)

    def insert_data(self, data, table_name, chunk_size=1000, empty_table=False):
        """
        Insert data into a SQL table.
    
        :param data: The data to insert.
        :type data: list[tuple]
        :param table_name: The name of the SQL table.
        :type table_name: str
        :param chunk_size: The number of rows to insert at a time.
        :type chunk_size: int
        :param empty_table: Whether to empty the table before inserting the data.
        :type empty_table: bool
        """
        # Get the column names from the data
        column_names = data[0]
        data = data[1:]
    
        # Empty the table if specified
        if empty_table:
            print(f"Emptying the table {table_name}...")
            self.delete_table_data(table_name)
            print(f"Table {table_name} emptied.")
    
        # Create the query to insert the data
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES "
    
        # Insert the data in chunks
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
    
            # Format values correctly as tuples
            values = ", ".join([f"({', '.join(map(repr, row))})" for row in chunk])
            chunk_query = query + values
    
            # print(f"Inserting chunk {i // chunk_size + 1} into {table_name}...")
            # print(f"SQL Query: {chunk_query}\n")  # Print the full SQL query
            self.execute_query(chunk_query)
            print(f"Chunk {i // chunk_size + 1} inserted.")
    
        print(f"All data inserted into {table_name}.")
    

    # Use insert_data method to insert data from a csv file
    def insert_csv_data(self, table_name, csv_file_path, empty_table=False):
        """
        Insert data from a CSV file into a SQL table.

        :param empty_table: Whether to empty the table before inserting the data.
        :type empty_table: bool
        :param table_name: The name of the SQL table.
        :type table_name: str
        :param csv_file_path: The path to the CSV file.
        :type csv_file_path: str
        """
        with open(csv_file_path, "r") as file:
            data = [line.strip().split(",") for line in file.readlines()]
            self.insert_data(data, table_name)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    sql = PyODBCSQL()
    result = sql.execute_query("SELECT 'Result' AS Test")
    print(result)
