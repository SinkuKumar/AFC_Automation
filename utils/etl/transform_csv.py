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

    def drop_textbox_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Drop the columns which start with textbox or Textbox.

        Args:
            df (pl.DataFrame): Input DataFrame.

        Returns:
            pl.DataFrame: DataFrame with text columns dropped.
        """
        return df.drop(
            [col for col in df.columns if col.lower().startswith("textbox")]
        )

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
        df.write_csv(processed_file)

    def fin_25(self, file_path:str, processed_file: str) -> None:
        """
        Transform the FIN_25 report.

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
        df.write_csv(processed_file)
