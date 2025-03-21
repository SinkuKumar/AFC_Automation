import os
import logging
import polars as pl

class TransformCSV:
    def __init__(self, client_id: int, date_time_stamp: str) -> None:
        self.client_id = client_id
        self.date_stamp = date_time_stamp.split()[0]
        self.time_stamp = date_time_stamp.split()[1]
        self.date_time_stamp = date_time_stamp

    def clean_currency_column(self, df: pl.DataFrame, column_names: str | list[str], decimals: int = 2) -> pl.DataFrame:
        """
        Cleans and converts currency columns in a Polars DataFrame to numeric values.

        This function performs the following transformations:
        - Strips leading and trailing whitespace.
        - Removes dollar signs (`$`) and commas (`,`).
        - Converts values enclosed in parentheses (e.g., `(123.45)`) to negative numbers (`-123.45`).
        - Casts the column to `Float64` and rounds to the specified number of decimal places.

        Args:
            df (pl.DataFrame): The Polars DataFrame containing the currency columns.
            column_names (str | list[str]): The name(s) of the column(s) to clean. 
                Can be a single column name (string) or a list of column names.
            decimals (int, optional): The number of decimal places to round the cleaned values. Defaults to 2.

        Returns:
            pl.DataFrame: A new DataFrame with cleaned currency columns.
        """
        logging.info("Starting currency column cleaning...")

        if isinstance(column_names, str):
            column_names = [column_names]

        try:
            for column in column_names:
                logging.info(f"Cleaning column: {column}")
                df = df.with_columns(
                    pl.col(column)
                    .str.strip_chars()
                    .str.replace_all(r"[\$,]", "")
                    .str.replace_all(r"^\((.*)\)$", r"-$1")
                    .cast(pl.Float64)
                    .round(decimals)
                    .alias(column)
                )
            logging.info("Currency column cleaning completed successfully.")
        except Exception as e:
            logging.error("An error occurred while cleaning currency columns.")
            raise

        return df

    def add_client_id_date_updated_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Add 'Client_ID' and 'Date_Updated' columns to the DataFrame.

        Args:
            df (pl.DataFrame): Input DataFrame.

        Returns:
            pl.DataFrame: Updated DataFrame with the new columns.
        """
        if "Client_ID" not in df.columns:
            df = df.with_columns([
                pl.lit(self.client_id).alias("Client_ID"),
                pl.lit(self.date_stamp).alias("Date_Updated")
            ])
        else:
            df = df.with_columns([
                pl.col("Client_ID").fill_null(self.client_id),
                pl.col("Date_Updated").fill_null(self.date_time_stamp),
            ])
        return df
    
    def drop_all_null_rows(self, frame: pl.DataFrame | pl.LazyFrame) -> pl.DataFrame | pl.LazyFrame:
        """Removes rows from a Polars DataFrame or LazyFrame where all columns contain only null (None) values.

        Args:
            frame (pl.DataFrame | pl.LazyFrame): Input DataFrame or LazyFrame to process.

        Returns:
            pl.DataFrame | pl.LazyFrame: DataFrame or LazyFrame with fully-null rows removed.

        Raises:
            TypeError: If the input is not a Polars DataFrame or LazyFrame.
        """
        if not isinstance(frame, (pl.DataFrame, pl.LazyFrame)):
            raise TypeError(f"Expected a polars DataFrame or LazyFrame, got {type(frame).__name__}")

        return frame.filter(~pl.all_horizontal(pl.all().is_null()))

    def sync_dataframe_with_table(self, table_columns: list[tuple[str]], df: pl.DataFrame) -> pl.DataFrame:
        """
        Aligns a Polars DataFrame with a database table by ensuring it has the same columns.
        Any extra columns in the DataFrame are removed, and missing columns are added with NULL values.

        Args:
            table_columns (list[tuple[str]]): The column names of the database table.
            df (pl.DataFrame): The Polars DataFrame to align.

        Returns:
            pl.DataFrame: A modified DataFrame that matches the database table schema.
        """
        try:            
            table_columns_lower = {col.lower(): col for sublist in table_columns for col in sublist}
            df_columns_lower = {col.lower(): col for col in df.columns}

            missing_columns = set(table_columns_lower.keys()) - set(df_columns_lower.keys())

            for col_lower in missing_columns:
                df = df.with_columns(pl.lit(None).alias(table_columns_lower[col_lower]))

            df = df.rename({df_columns_lower[col_lower]: table_columns_lower[col_lower] for col_lower in df_columns_lower if col_lower in table_columns_lower})

            flat_table_columns = [col for sublist in table_columns for col in sublist]
            df = df.select(flat_table_columns)

            logging.info("Aligned DataFrame to match database table and dataframe columns")
            return df

        except Exception as e:
            logging.error(f"Error while aligning DataFrame with database table: {e}")
            raise

    def drop_textbox_columns(self, df: pl.DataFrame, skip_columns: list[str] = []) -> pl.DataFrame:
        """
        Drop the columns which start with textbox or Textbox.

        Args:
            df (pl.DataFrame): Input DataFrame.

        Returns:
            pl.DataFrame: DataFrame with text columns dropped.
        """
        return df.drop(
            [col for col in df.columns if col.lower().startswith("textbox") and col not in skip_columns]
        )
    
    def combine_csv_files(self, folder_path: str, output_file: str, start_with: str = None) -> None:
        """
        Combines multiple CSV files in a given folder into a single CSV file.

        Args:
            folder_path (str): Path to the folder containing CSV files.
            output_file (str): Path where the combined CSV file will be saved.
            start_with (str, optional): If provided, only files that start with this prefix will be combined.

        Returns:
            None

        Raises:
            FileNotFoundError: If no matching CSV files are found in the folder.
        """
        all_files = [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.endswith('.csv') and (start_with is None or f.startswith(start_with))
        ]
        
        if not all_files:
            raise FileNotFoundError("No matching CSV files found.")
        
        df_list = [pl.read_csv(file) for file in all_files]
        combined_df = pl.concat(df_list)
        combined_df.write_csv(output_file)
        
        logging.info(f" Combined {len(all_files)} CSV files.")

    def cnt_27(self, file_path: str, processed_file: str) -> None:
        """
        Transform the CNT_27 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {
            "Svc_Date": "Service_Date",
            "Status_Name": "Status",
            "ArrivalStatus": "Arrival_Status",
            "Class": "Financial_Class",
            "Pat_Num": "Patient_Num",
            "Pat_Name": "Patient_Name",
            "Rendering_Phy": "Rendering_Physician",
            "SignOffSealedDate": "Chart_Signed_Date",
            "Inv_Num": "Invoice_Num",
        }

        # df = df.rename(columns_to_rename)
        df = self.clean_currency_column(df, "Total_Charge")
        df = self.add_client_id_date_updated_columns(df)
        # TODO: Sync columns from table to df before writing to CSV
        df.write_csv(processed_file)

    def cnt_19(self, file_path: str, processed_file: str) -> None:
        """
        Transform the CNT_19 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        # TODO: Add column renaming and other transformations
        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.drop_textbox_columns(df)
        df = self.add_client_id_date_updated_columns(df)
        # TODO: Sync columns from table to df before writing to CSV
        df.write_csv(processed_file)

    def adj_4(self, file_path: str, processed_file: str) -> None:
        """
        Transform the ADJ_4 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """

        df = pl.read_csv(file_path, infer_schema_length=0, skip_lines=3)
        df = df.slice(3)
        df = self.drop_textbox_columns()

        df.write_csv(processed_file)


    def adj_11(self, file_path: str, processed_file: str) -> None:
        """
        Transform the ADJ_11 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.drop_textbox_columns(df)
        df = self.clean_currency_column(df, "Adj_Amt")
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)

    def fin_18(self, file_path: str, processed_file: str) -> None:
        """
        Transform the FIN_18 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.clean_currency_column(df, ["Total_Charge", "Rebilled_Total_Charge"])
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)

    def pay_41(self, file_path: str, processed_file: str) -> None:
        """
        Transform the PA?Y_41 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.drop_textbox_columns(df)
        df = self.clean_currency_column(df, ["Payment"])
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)

    def xry_03(self, file_path: str, processed_file: str) -> None:
        """
        Transform the PA?Y_41 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.

        Returns:
            None
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)

    def fin_25(self, file_path: str, processed_file: str, table_columns: list[tuple[str]]) -> None:
        """
        Transform the FIN_25 report.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the processed CSV file.
            table_columns list[tuple[str]]: The column names of the specified table.
            
        Returns:
            None
        """
        try:
            logging.info("Fin_25 Data transformation process started.")
            df = pl.read_csv(file_path, infer_schema_length=0)
            df = self.drop_all_null_rows(df)

            df = df.rename({"Textbox2":"Svc_Date"})
            df = df.with_columns(pl.col("Svc_Date").str.to_date(format="%m/%d/%Y", strict=False))

            df = df.with_columns(df["Proc_Code"].str.split(" | ").alias("split_data"))
            df = df.explode("split_data")
            df = df.with_columns(
                df["split_data"].str.split(": ").alias("split_key_value")
            ).select(
                pl.all().exclude("split_data"),
                pl.col("split_key_value").list.get(0).alias("new_proc_code"),
                pl.col("split_key_value").list.get(1).alias("Proc_Amount")
            )

            df = df.drop(["split_key_value", "Proc_Code"])
            df = df.rename({"new_proc_code": "Proc_Code"})

            df = self.clean_currency_column(df, ["Total_Charge", "Copay_Paid", "Curr_Pay_Amt", "Other_Paid", "Total_Adj", "Crg_Balance", "Proc_Amount"])

            df = df.with_columns(
                pl.col("Pat_Name").str.replace_all(",", "").alias("Pat_Name"),
                pl.col("Rendering_Phy").str.replace_all(",", "").alias("Rendering_Phy")
            )

            df = self.add_client_id_date_updated_columns(df)
            df = self.sync_dataframe_with_table(table_columns, df)

            df.write_csv(processed_file)
            logging.info("Fin_25 Data transformation process completed.")
        except Exception as e:
            logging.error("Error occurred during Fin_25 data transformation.")
            raise

    def pay_10(self, file_path:str, processed_file: str, table_columns: list[tuple[str]]) -> None:
        """
        Transform the PAY_10 report.

        This function performs the following operations:
        - Reads the CSV into a Polars DataFrame with specified Columns.
        - Removes rows where all columns contain only null (None) values.
        - Renames the `textbox18`, `textbox22` columns to `Charge_Amt`, `Net_AR` respectively.
        - Cleans currency columns using `clean_currency_column`.
        - Converts `Svc_Date` to a date.
        - Adds a new columns `Client_id`, `Date_Updated` with the provided client ID, current date and time respectively.
        - Aligns DataFrame with a database table.
        - Writes the cleaned DataFrame to an output CSV file.

        Args:
            file_path (str): Path to the input CSV file.
            processed_file (str): Path to save the cleaned output CSV file.
            table_columns list[tuple[str]]: The column names of the specified table.

        Returns:
            None
        """
        try:
            logging.info("Pay_10 Data transformation process started.")
            df = pl.read_csv(file_path, columns=["Payer_Class", "Payer_Name", "Pat_Name", "Svc_Date", "CPT_Code", "textbox18", "Paid_Amt", "Adj_Amt", "textbox22"], infer_schema_length=0)
            df = self.drop_all_null_rows(df)

            df = df.rename({"textbox18":"Charge_Amt", "textbox22":"Net_AR"})
            df = self.clean_currency_column(df, ["Charge_Amt", "Paid_Amt", "Adj_Amt", "Net_AR"])

            df = df.with_columns(
                pl.col("Payer_Name").str.replace_all(",", "").alias("Payer_Name"),
                pl.col("Pat_Name").str.replace_all(",", "").alias("Pat_Name")
            )

            df = df.with_columns(pl.col("Svc_Date").str.to_date(format="%m/%d/%Y", strict=False))
            df = self.add_client_id_date_updated_columns(df)

            df = self.sync_dataframe_with_table(table_columns, df)
            df.write_csv(processed_file)
            logging.info("Pay_10 Data transformation process completed.")
        except Exception as e:
            logging.error("Error occurred during Pay_10 data transformation.")
            raise

    def rev_19(self, file_path:str, processed_file: str, table_columns: list[tuple[str]]) -> None:
        """
        Transform the REV_19 report.

        This function performs the following operations:
        - Reads the CSV into a Polars DataFrame with specified Columns.
        - Removes rows where all columns contain only null (None) values.
        - Removes all the commas(,) from the `Phy_Name` column.
        - Cleans currency columns using `clean_currency_column`.
        - Adds a new columns `Client_id`, `Date_Updated` with the provided client ID, current date and time respectively.
        - Aligns DataFrame with a database table.
        - Writes the cleaned DataFrame to an output CSV file.

        Args:
            input_csv_data_file (str): Path to the input CSV file.
            output_csv_data_path (str): Path to save the cleaned output CSV file.
            client_id (int): Client ID to be added as `client_id` in the DataFrame.

        Returns:
            None
        """
        try:
            logging.info("Rev_19 Data transformation process started.")
            df = pl.read_csv(file_path, columns=["Phy_Name", "Rev_Type", "Proc_Code", "Description", "Charge_Amt"], infer_schema_length=0)
            df = self.drop_all_null_rows(df)

            df = df.with_columns(pl.col("Phy_Name").str.replace_all(",", "").alias("Phy_Name"))
            df = self.clean_currency_column(df, ['Charge_Amt'])
            df = self.add_client_id_date_updated_columns(df)

            df = self.sync_dataframe_with_table(table_columns, df)
            df.write_csv(processed_file)
            logging.info("Rev_19 Data transformation process completed.")
        except Exception as e:
            logging.error("Error occurred during Rev_19 data transformation.")
            raise
    
    def ccr_03(self, file_path:str, processed_file: str) -> None:
        """
        Transform CCR_03 Report
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.drop_textbox_columns(df)
        df = self.clean_currency_column(df, 'ReserveAmt')
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)

    def ccr_02(self, file_path:str, processed_file: str) -> None:
        """
        Transform CCR_02 Report
        """
        df = pl.read_csv(file_path, infer_schema_length=0)

        columns_to_rename = {

        }

        # df = df.rename(columns_to_rename)
        df = self.drop_textbox_columns(df)
        df = self.clean_currency_column(df, 'Payment_Amt')
        df = self.add_client_id_date_updated_columns(df)
        df.write_csv(processed_file)
    
    def pat_20(self):
        """
        Need clarification

        TODO: Ask AFC Team what Textbox32 columns represents, what to rename
        """
        pass