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
import logging
import utils.error_messages as em

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
            f"""DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};
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

    def get_users_credentials(self, client_ids: list[int]) -> list[tuple[str, str]]:
        """
        Fetches the usernames and passwords of active clients from the MSSQL database.

        Args:
            client_ids (List[int]): List of client IDs whose credentials need to be fetched.

        Returns:
            list[tuple[str, str]]: A list of tuples, where each tuple contains (Username, Password).

        Raises:
            ValueError: If the client_ids list is empty.
            Exception: If there is a database error.
        """
        if not client_ids:
            logging.warning("Empty client_ids list provided.")
            raise ValueError("Client ID list cannot be empty.")

        try:
            ids_str = ','.join(map(str, client_ids))
            query = f"SELECT client_id, Username, Password FROM bi_afc.dbo.afc_password_tbl WHERE active = 1 and client_id IN ({ids_str})"
            results = self.execute_query(query)
            logging.info("Successfully retrieved user credentials.")
            return [(row[0], row[1], row[2]) for row in results]

        except pyodbc.Error as e:
            logging.error(f"Database error occurred while fecthing users credentials: {e}")
            raise

    def csv_bulk_insert(self, output_csv_path: str, table_name: str) -> None:
        """
        Load data from a CSV file into a database table.

        This function reads data from a CSV file and inserts it into the specified database table 
        using the provided connection string.

        Args:
            output_csv_path (str): The path to the CSV file containing the data to be loaded.
            table_name (str): The name of the target database table.

        Returns:
            None
        """
        try:
            sql = f"""
            BULK INSERT {table_name}
            FROM '{output_csv_path}'
            WITH (
                FORMAT = 'CSV',
                FIELDTERMINATOR = ',', 
                ROWTERMINATOR = '\n',
                FIRSTROW = 2
            );
            """
            self.execute_query(sql)
            logging.info(f"Records inserted successfully.")
        except pyodbc.Error as e:
            logging.error(f"Code: {em.DATA_LOAD_ISSUE} | Message : Database operation failed while bulk insert into database.")
            raise
    
    def get_all_active_client_ids(self) -> None:
        """
        Retrieves all active Client IDs from the Database table.

        Args:
            None
        
        Returns:
            list: A list of active Client IDs.
        """
        try:
            logging.info("Fetching all Client IDs from Databse table.")
            client_ids_result = self.execute_query("select client_id from bi_afc.dbo.afc_password_tbl where active = 1;")
            client_ids = [client_id[0] for client_id in client_ids_result]
            logging.info("Successfully retrieved %d Client IDs.", len(client_ids))
            return client_ids
        except Exception as e:
            logging.error("Failed to retrieve Client IDs: %s", str(e))
            raise

    def check_and_create_table(self, table_name, create_table_query):
        """
        Checks if a table exists in the database and creates it if it does not exist.

        Args:
            table_name (str): The name of the table to check.
            create_table_query (str): The SQL query to create the table if it does not exist.

        Returns:
            None
        """
        try:
            logging.info("Checking if table '%s' exists.", table_name)
            
            result = self.execute_query(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}';")
            table_exists = result[0][0]

            if table_exists == 1:
                logging.info("Table '%s' already exists.", table_name)
            elif table_exists == 0:
                logging.info("Table '%s' does not exist. Creating table...", table_name)
                self.execute_query(create_table_query)
                logging.info("Table '%s' has been successfully created.", table_name)
        except Exception as e:
            logging.error("Error checking or creating table '%s': %s", table_name, str(e))
            raise

    def delete_table_data(self, table_name: str, client_id: int) -> None:
        """
        Deletes all data for particular client_id from the specified database table.

        This method executes a SQL `DELETE` statement to remove all rows of the particular client_id from the given table. 

        Args:
            table_name (str): The name of the table from which data should be deleted.
            client_id (int): Client ID for which the data to be deleted.

        Returns:
            None

        Raises:
            pyodbc.Error: If an error occurs while executing the SQL query.
        """
        try:
            query = f"DELETE FROM {table_name} where Client_id = {client_id}"
            self.execute_query(query)
            logging.info(f"Successfully deleted table data for client : {client_id}.")

        except pyodbc.Error as e:
            logging.error(f"Database error occurred while deleting the table data: {e}")
            raise

    def truncate_table(self, table_name: str) -> None:
        """
        Deletes all data for particular client_id from the specified database table.

        This method executes a SQL `DELETE` statement to remove all rows of the particular client_id from the given table. 

        Args:
            table_name (str): The name of the table from which data should be deleted.

        Returns:
            None

        Raises:
            pyodbc.Error: If an error occurs while executing the SQL query.
        """
        try:
            query = f"TRUNCATE TABLE {table_name};"
            self.execute_query(query)
            logging.info(f"Successfully deleted table data.")

        except pyodbc.Error as e:
            logging.error(f"Database error occurred while deleting the table data: {e}")
            raise

        

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    sql = PyODBCSQL()
    result = sql.execute_query("SELECT 'Result' AS Test")
    print(result)
