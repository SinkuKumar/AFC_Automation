def pay_10_create_query(table_name):
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

def rev_19_create_query(table_name):
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