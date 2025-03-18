import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.pyodbc_sql import PyODBCSQL

class BulkLoadSQL:
    def __init__(self, sql: PyODBCSQL, empty_table: bool = False) -> None:
        self.sql = sql
        self.empty_table = empty_table
    
    def clear_table(self, table: str) -> None:
        """
        Clear the entire table.
        """
        self.sql.execute_query("TRUNCATE TABLE {}".format(table))

    def clear_client_data(self, client_id: int, table_name: int) -> None:
        """
        Clear the client data.
        """
        self.sql.execute_query("DELETE FROM {table_name} WHERE ClientID = {client_id}".format(table_name, client_id))

    def prepare_staging_table(self, base_table: str, staging_table: str) -> None:
        """
        Prepare the table to perform bulk load.
        Check if the table exists, if not create the table.
        Clear the table if `clear_table` is set to True.
        """
        table_exists = False
        try:
            table_exists = self.sql.execute_query("SELECT TOP 1 * FROM {}".format(staging_table))
        except:
            table_exists = False

        if not table_exists:
            self.sql.execute_query("SELECT TOP 0 * INTO {} FROM {}".format(staging_table, base_table))
        
        if self.empty_table:
            self.clear_table(staging_table)
    
    def load_report(self, processed_file: str, base_table, staging_table: str) -> None:
        """
        Bulk load the report into the database.
        """
        self.prepare_staging_table(base_table, staging_table)
        self.sql.csv_bulk_insert(processed_file, staging_table)
