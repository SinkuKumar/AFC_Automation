"""
SQL Table Creation Module

This module contains functions to generate SQL `CREATE TABLE` statements for various staging tables.
Each function returns a formatted SQL string to create a table with predefined columns.

Functions:
    - pay_10_create_query: Generates SQL for the `PAY_10_Staging_Base` table.
    - rev_19_create_query: Generates SQL for the `REV_19_Staging_Base` table.
    - cnt_27_create_query: Generates SQL for the `CNT_27_Staging_Base` table.
    - cnt_19_create_query: Generates SQL for the `CNT_19_Staging_Base` table.
    - ccr_03_create_query: Generates SQL for the `CCR_03_Staging_Base` table.
    - ccr_02_create_query: Generates SQL for the `CCR_02_Staging_Base` table.
"""


def pay_10_create_query(table_name='PAY_10_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for a payer-related table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Payer_Class  VARCHAR(50),
        Payer_Name  VARCHAR(60),
        Pat_Name  VARCHAR(60),
        Svc_Date DATE,
        CPT_Code  VARCHAR(20),
        Charge_Amt  DECIMAL(10,2),
        Paid_Amt  DECIMAL(10,2),
        Adj_Amt  DECIMAL(10,2),
        Net_AR  DECIMAL(10,2),
        Client_id  INT,
        Date_Updated datetime
    );
    """


def rev_19_create_query(table_name='REV_19_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for a revenue-related table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Phy_Name  VARCHAR(50),
        Rev_Type  VARCHAR(30),
        Proc_Code  VARCHAR(20),
        "Description" VARCHAR(60),
        Charge_Amt  DECIMAL(10,2),
        Client_id  INT,
        Date_Updated datetime
    );
    """


def cnt_27_create_query(table_name='CNT_27_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for the `CNT_27_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CNT_27_Staging_Base).
    :type table_name: str, optional
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name} (
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Time_In NVARCHAR(MAX),
        Time_Out NVARCHAR(MAX),
        Status_Name NVARCHAR(MAX),
        ArrivalStatus NVARCHAR(MAX),
        Class NVARCHAR(MAX),
        Payer_Type NVARCHAR(MAX),
        Payer NVARCHAR(MAX),
        Member_ID NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        Pat_Name NVARCHAR(MAX),
        Visit_Type NVARCHAR(MAX),
        Rendering_Phy NVARCHAR(MAX),
        SignOffSealedDate NVARCHAR(MAX),
        Log_Num NVARCHAR(MAX),
        Inv_Num NVARCHAR(MAX),
        Withhold_Code NVARCHAR(MAX),
        Total_Charge NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
"""


def cnt_19_create_query(table_name='CNT_19_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for the `CNT_19_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CNT_19_Staging_Base).
    :type table_name: str, optional
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Category NVARCHAR(MAX),
        Clinic NVARCHAR(MAX),
        Type NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        Last_Name NVARCHAR(MAX),
        First_Name NVARCHAR(MAX),
        Middle_Name NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def ccr_03_create_query(table_name='CCR_03_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for the `CCR_03_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CCR_03_Staging_Base).
    :type table_name: str, optional
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name} (
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        DaysSinceTransaction NVARCHAR(MAX),
        Pat_Name NVARCHAR(MAX),
        Pymt_Type NVARCHAR(MAX),
        ReserveAmt FLOAT,
        Crt_UserID NVARCHAR(MAX),
        Card_Type NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def ccr_02_create_query(table_name='CCR_02_Staging_Base'):
    """
    Generates a SQL `CREATE TABLE` statement for the `CCR_02_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CCR_02_Staging_Base).
    :type table_name: str, optional
    :return: SQL query string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name} (
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Type NVARCHAR(MAX),
        Inv_Num NVARCHAR(MAX),
        Pat_Name NVARCHAR(MAX),
        Payment_Amt FLOAT,
        Crt_UserID NVARCHAR(MAX),
        Reversed NVARCHAR(MAX),
        Card_Type NVARCHAR(MAX),
        Payment_Plan NVARCHAR(MAX),
        Payment_Type NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


if __name__ == '__main__':
    print(pay_10_create_query('PAY_10_Staging_Base'))
    print(ccr_03_create_query())
    print(ccr_02_create_query())
