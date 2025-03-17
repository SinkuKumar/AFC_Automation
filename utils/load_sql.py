import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.pyodbc_sql import PyODBCSQL

class BulkLoadSQL:
    def __init__(self, sql: PyODBCSQL, clear_table: bool = False) -> None:
        self.sql = sql
        self.clear_table = clear_table
    
    def clear_table(self, table: str) -> None:
        """
        Clear the staging table.
        """
        self.sql.execute_query("TRUNCATE TABLE {}".format(table))
    
    def cnt_27(self, file_path: str, staging_table: str) -> None:
        """
        Bulk load the CNT_27 report into the database.
        """
        if self.clear_table:
            self.clear_table(staging_table)
        self.sql.bulk_load_csv(file_path, staging_table)

        