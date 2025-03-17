import os
import time
import polars as pl

def convert_money_column(df: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Convert a money column with values like '$1,080.00' into float.

    Args:
        df (pl.DataFrame): Input DataFrame.
        column (str): Column name containing money values.

    Returns:
        pl.DataFrame: Updated DataFrame with the column converted to float.
    """
    return df.with_columns(
        pl.col(column)
        .str.replace_all(r"[\$,]", "")  # Remove '$' and ',' from values
        .cast(pl.Float64)  # Convert to float
    )

def add_client_id_date_updated_columns(df: pl.DataFrame, client_id: int, date_stamp: str) -> pl.DataFrame:
    """
    Add 'Client_ID' and 'Date_Updated' columns to the DataFrame.

    Args:
        df (pl.DataFrame): Input DataFrame.
        client_id (int): Client ID.
        date_stamp (str): Date stamp.

    Returns:
        pl.DataFrame: Updated DataFrame with the new columns.
    """
    if "Client_ID" not in df.columns:
        df = df.with_columns([
            pl.lit(client_id).alias("Client_ID"),
            pl.lit(date_stamp).alias("Date_Updated")
        ])
    else:
        df = df.with_columns([
            pl.col("Client_ID").fill_null(client_id),
            pl.col("Date_Updated").fill_null(date_stamp),
        ])
    return df

def cnt_27(file_path: str, client_id: int, date_stamp: str, time_stamp: str) -> None:
    """
    Transform the CNT_27 report.
    
    Args:
        file_path (str): Path to the CSV file.
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
    df = convert_money_column(df, "Total_Charge")
    df = add_client_id_date_updated_columns(df, client_id, date_stamp)
    time.sleep(100)
    processed_file = os.path.join(os.path.dirname(file_path), f"CNT_27_Processed_{time_stamp}.csv")
    df.write_csv(processed_file)

if __name__ == "__main__":
    client_id = 3622
    date_stamp = "2024-06-06"
    file_path = "/Users/Sinku/Development/AFC_Automation/Downloads/3622/CNT_27_LogBookVisits.csv"
    cnt_27(file_path, client_id, date_stamp)