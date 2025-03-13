import logging
import datetime
import polars as pl

from utils.pyodbc_sql import PyODBCSQL
DB = PyODBCSQL()

def clean_currency_column(df: pl.DataFrame, column_names: str | list[str], decimals: int = 2) -> pl.DataFrame:
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

def drop_all_null_rows(frame: pl.DataFrame | pl.LazyFrame) -> pl.DataFrame | pl.LazyFrame:
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

def sync_dataframe_with_table(table_columns: list, df: pl.DataFrame) -> pl.DataFrame:
        """
        Aligns a Polars DataFrame with a database table by ensuring it has the same columns.
        Any extra columns in the DataFrame are removed, and missing columns are added with NULL values.

        Args:
            table_columns (list): The column names of the database table.
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

            flat_table_columns = [col for sublist in table_columns for col in sublist]
            df = df.select(flat_table_columns)

            logging.info("Aligned DataFrame to match database table and dataframe columns")
            return df

        except Exception as e:
            logging.error(f"Error aligning DataFrame: {e}")
            raise

def fin_25_report_data_transformation(input_csv_data_file: str, output_csv_data_path: str, client_id: int) -> None:
    """
    Processes a CSV file and generates a cleaned report.

    This function performs the following operations:
    - Reads the CSV into a Polars DataFrame.
    - Renames the `Textbox2` column to `svc_date` and converts it to a date.
    - Removes rows where all columns contain only null (None) values
    - Adds a new column `updated_date` with the current date.
    - Splits the `Proc_Code` column on " | " into 'proc_code' and 'proc_amount'.
    - Adds a new column `client_id` with the provided client ID.
    - Cleans currency columns using `clean_currency_column`.
    - Writes the cleaned DataFrame to an output CSV file.

    Args:
        input_csv_data_file (str): Path to the input CSV file.
        output_csv_data_path (str): Path to save the cleaned output CSV file.
        client_id (int): Client ID to be added as `client_id` in the DataFrame.

    Returns:
        None
    """
    try:
        logging.info("Data transformation process started.")
        df = pl.read_csv(input_csv_data_file)

        df = df.rename({"Textbox2":"svc_date"})
        df = df.with_columns(pl.col("svc_date").str.to_date(format="%m/%d/%Y", strict=False))
        df = drop_all_null_rows(df)
        df = df.with_columns(pl.lit(datetime.date.today()).alias("updated_date"))

        df = df.with_columns(df["Proc_Code"].str.split(" | ").alias("split_data"))
        df = df.explode("split_data")
        df = df.with_columns(
            df["split_data"].str.split(": ").alias("split_key_value")
        ).select(
            pl.all().exclude("split_data"),
            pl.col("split_key_value").list.get(0).alias("new_proc_code"),
            pl.col("split_key_value").list.get(1).alias("proc_amount")
        )

        df = df.drop(["split_key_value", "Proc_Code"])
        df = df.rename({"new_proc_code": "proc_code"})

        df = df.with_columns(pl.lit(client_id).alias("client_id"))
        df = clean_currency_column(df, ["Total_Charge", "Copay_Paid", "Curr_Pay_Amt", "Other_Paid", "Total_Adj", "Crg_Balance", "proc_amount"])

        df = df.with_columns(
            pl.col("Pat_Name").str.replace_all(",", "").alias("Pat_Name"),
            pl.col("Rendering_Phy").str.replace_all(",", "").alias("Rendering_Phy")
        )

        df.write_csv(output_csv_data_path)
        logging.info("Data transformation process completed.")
    except Exception as e:
        logging.error("Error occurred during data transformation.")
        raise

def pay_10_report_data_transformation(input_csv_data_file: str, output_csv_data_path: str, table_name, client_id: int) -> None:
    """
    Processes a CSV file and generates a cleaned report.

    This function performs the following operations:
    - Reads the CSV into a Polars DataFrame with specified Columns.
    - Removes rows where all columns contain only null (None) values.
    - Renames the `textbox18`, `textbox22` columns to `Charge_Amt`, `Net_AR` respectively.
    - Cleans currency columns using `clean_currency_column`.
    - Adds a new column `Date_Updated` with the current date and time.
    - Converts `Svc_Date` to a date.
    - Adds a new column `Client_id` with the provided client ID.
    - Writes the cleaned DataFrame to an output CSV file.

    Args:
        input_csv_data_file (str): Path to the input CSV file.
        output_csv_data_path (str): Path to save the cleaned output CSV file.
        client_id (int): Client ID to be added as `client_id` in the DataFrame.

    Returns:
        None
    """
    try:
        logging.info("Data transformation process started.")
        df = pl.read_csv(input_csv_data_file, columns=["Payer_Class", "Payer_Name", "Pat_Name", "Svc_Date", "CPT_Code", "textbox18", "Paid_Amt", "Adj_Amt", "textbox22"])
        df = drop_all_null_rows(df)

        df = df.rename({"textbox18":"Charge_Amt", "textbox22":"Net_AR"})
        df = clean_currency_column(df, ["Charge_Amt", "Paid_Amt", "Adj_Amt", "Net_AR"])

        df = df.with_columns(
            pl.col("Payer_Name").str.replace_all(",", "").alias("Payer_Name"),
            pl.col("Pat_Name").str.replace_all(",", "").alias("Pat_Name")
        )

        df = df.with_columns(pl.col("Svc_Date").str.to_date(format="%m/%d/%Y", strict=False))
        df = df.with_columns(pl.lit(datetime.datetime.now()).alias("Date_Updated"))

        df = df.with_columns(pl.lit(client_id).alias("Client_id"))

        table_columns = DB.get_column_names(table_name)

        df = sync_dataframe_with_table(table_columns, df)
        df.write_csv(output_csv_data_path)
        logging.info("Data transformation process completed.")
    except Exception as e:
        logging.error("Error occurred during data transformation.")
        raise