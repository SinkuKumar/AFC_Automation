"""
SQL Table Creation Module

This module contains functions to generate SQL `CREATE TABLE` statements for various staging tables.
Each function returns a formatted SQL string to create a table with predefined columns.

Functions:
    - pay_10_staging_table: Generates SQL for the `PAY_10_Staging_Base` table.
    - rev_19_staging_table: Generates SQL for the `REV_19_Staging_Base` table.
    - cnt_27_staging_table: Generates SQL for the `CNT_27_Staging_Base` table.
    - cnt_19_staging_table: Generates SQL for the `CNT_19_Staging_Base` table.
    - ccr_03_staging_table: Generates SQL for the `CCR_03_Staging_Base` table.
    - ccr_02_staging_table: Generates SQL for the `CCR_02_Staging_Base` table.
"""


def cnt_27_staging_table(table_name="CNT_27_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a CNT_27 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
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
        Total_Charge FLOAT,
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def cnt_19_staging_table(table_name="CNT_19_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a CNT_19 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
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


def adj_11_staging_table(table_name="ADJ_11_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a ADJ_11 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Inv_Num NVARCHAR(MAX),
        Clinic NVARCHAR(MAX),
        Rev_Type NVARCHAR(MAX),
        Trans_Date NVARCHAR(MAX),
        Phy_Name NVARCHAR(MAX),
        Proc_Code NVARCHAR(MAX),
        Payer NVARCHAR(MAX),
        Payer_Name NVARCHAR(MAX),
        Adj_Amt FLOAT,
        Reason NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def fin_18_staging_table(table_name="FIN_18_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a FIN_18 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Inv_Num NVARCHAR(MAX),
        Log_Num NVARCHAR(MAX),
        Type NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        Pat_Name NVARCHAR(MAX),
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Phy_Name NVARCHAR(MAX),
        Prev_Payer_Name NVARCHAR(MAX),
        Total_Charge FLOAT,
        New_Inv_Num NVARCHAR(MAX),
        Rebilled_To_Payer NVARCHAR(MAX),
        Rebilled_Total_Charge FLOAT,
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def pay_41_staging_table(table_name="PAY_41_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PAY_41 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Clinic NVARCHAR(MAX),
        Payer_Name NVARCHAR(MAX),
        Patient_Name NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Inv_Num NVARCHAR(MAX),
        Trans_Date NVARCHAR(MAX),
        Proc_Code NVARCHAR(MAX),
        Proc_Description NVARCHAR(MAX),
        Financial_Class NVARCHAR(MAX),
        Reason NVARCHAR(MAX),
        Payment FLOAT,
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def pay_10_staging_table(table_name="PAY_10_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PAY_10 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
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


def xry_03_staging_table(table_name="XRY_03_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a XRY_03 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Past_Due NVARCHAR(MAX),
        DOS NVARCHAR(MAX),
        Patient_Number NVARCHAR(MAX),
        Patient_First NVARCHAR(MAX),
        Patient_Last NVARCHAR(MAX),
        Reading_By NVARCHAR(MAX),
        Clinic NVARCHAR(MAX),
        CPT NVARCHAR(MAX),
        Xray_Ordered NVARCHAR(MAX),
        Status NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def ccr_02_staging_table(table_name="CCR_02_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for the `CCR_02_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CCR_02_Staging_Base).
    :type table_name: str, optional
    :returns: SQL table string.
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


def ccr_03_staging_table(table_name="CCR_03_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for the `CCR_03_Staging_Base` table.

    :param table_name: The name of the table to be created (default: CCR_03_Staging_Base).
    :type table_name: str, optional
    :returns: SQL table string.
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


def per_2_staging_table(table_name="PER_2_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PER_2 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Clinic NVARCHAR(MAX),
        Date_In NVARCHAR(MAX),
        Patient_Name NVARCHAR(MAX),
        Provider NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        Time_In NVARCHAR(MAX),
        Time_In_By NVARCHAR(MAX),
        Vitals_Time NVARCHAR(MAX),
        Vitals_By NVARCHAR(MAX),
        Time_In_To_Time_Vitals    NVARCHAR(MAX),
        Discharged_Time    NVARCHAR(MAX),
        Discharged_By    NVARCHAR(MAX),
        Time_Vitals_To_Time_Discharge    NVARCHAR(MAX),
        Time_In_To_Time_Discharge    NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def med_01_staging_table(table_name="MED_01_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a MED_01 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        SignedOffBy NVARCHAR(MAX),
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        Pat_Name NVARCHAR(MAX),
        PrescribedDate NVARCHAR(MAX),
        PrescribedBy NVARCHAR(MAX),
        DrugName NVARCHAR(MAX),
        Strength NVARCHAR(MAX),
        StrengthUOM NVARCHAR(MAX),
        DispenseQuantity NVARCHAR(MAX),
        IsDispensed    NVARCHAR(MAX),
        IsEPrescribe NVARCHAR(MAX),
        IsPrintPhone NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def pat_20_staging_table(table_name="PAT_20_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PAT_20 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Description NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        Last_Name NVARCHAR(MAX),
        Sex    NVARCHAR(MAX),
        Address1    NVARCHAR(MAX),
        Address2    NVARCHAR(MAX),
        City    NVARCHAR(MAX),
        State    NVARCHAR(MAX),
        Zip    NVARCHAR(MAX),
        Pat_Phone    NVARCHAR(MAX),
        Cell_Phone    NVARCHAR(MAX),
        Email    NVARCHAR(MAX),
        Last_Clinic  NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def lab_01_staging_table(table_name="LAB_01_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a LAB_01 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
        Clinic NVARCHAR(MAX),
        Svc_Date NVARCHAR(MAX),
        OrderedByPhysicianOn NVARCHAR(MAX),
        Pat_Num NVARCHAR(MAX),
        First_Name NVARCHAR(MAX),
        Last_Name NVARCHAR(MAX),
        OrderedByPhysician NVARCHAR(MAX),
        Code NVARCHAR(MAX),
        TestName NVARCHAR(MAX),
        Status NVARCHAR(MAX),
        FacilityName NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def cht_02_staging_table(table_name="CHT_02_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a CHT_02 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
    	Clinic	NVARCHAR(MAX),
	    Pat_Num	NVARCHAR(MAX),
	    Svc_Date	NVARCHAR(MAX),
	    VisitType	NVARCHAR(MAX),
	    CreatedBy2	NVARCHAR(MAX),
	    SignedOffBy2	NVARCHAR(MAX),
	    SignedOffSealedBy2	NVARCHAR(MAX),
	    LastUpdatedBy1	NVARCHAR(MAX),
	    EMCode	NVARCHAR(MAX),
	    EMCodeSuggested	NVARCHAR(MAX),
	    EmCodeOverride	NVARCHAR(MAX),
	    DiagnosisLevel1	NVARCHAR(MAX),
	    DiagnosisText	NVARCHAR(MAX),
	    ICD10	NVARCHAR(MAX),
	    CodeDescription	NVARCHAR(MAX),
	    DiagnosisType	NVARCHAR(MAX),
	    DiagnosisCategory	NVARCHAR(MAX),
	    DiagnosisSeverity	NVARCHAR(MAX),
	    DifferentialDiagnosis	NVARCHAR(MAX),
	    DifferentialDiagnosisText1	NVARCHAR(MAX),
	    UncertainPrognosis1	NVARCHAR(MAX),
	    DifferentialDiagnosisText2	NVARCHAR(MAX),
	    UncertainPrognosis2	NVARCHAR(MAX),
	    DifferentialDiagnosisText3	NVARCHAR(MAX),
	    UncertainPrognosis3	NVARCHAR(MAX),
	    DifferentialDiagnosisText4	NVARCHAR(MAX),
	    UncertainPrognosis4	NVARCHAR(MAX),
	    DifferentialDiagnosisText5	NVARCHAR(MAX),
	    UncertainPrognosis5	NVARCHAR(MAX),
	    Risk	NVARCHAR(MAX),
	    RiskText	NVARCHAR(MAX),
	    RiskSuggested	NVARCHAR(MAX),
	    RiskOverride	NVARCHAR(MAX),
	    RiskOverrideBy	NVARCHAR(MAX),
	    RiskRxReason	NVARCHAR(MAX),
	    RiskRxNotes	NVARCHAR(MAX),
	    DataReviewLevel	NVARCHAR(MAX),
	    DataReviewText	NVARCHAR(MAX),
	    DRTestsOrdered	NVARCHAR(MAX),
	    DRTestsReviewed	NVARCHAR(MAX),
	    DRExternalSourcesReviewed	NVARCHAR(MAX),
	    DRExternalSources	NVARCHAR(MAX),
	    DRAssessReqIndepHistorian	NVARCHAR(MAX),
	    DRIndepInterpTests	NVARCHAR(MAX),
	    DRDiscussMgmtTestInterp	NVARCHAR(MAX),
	    TimeLevel	NVARCHAR(MAX),
	    TimeText	NVARCHAR(MAX),
	    EMCodeTimeAddOnCode	NVARCHAR(MAX),
	    EMCodeTimeAddOnCodeQuantity	NVARCHAR(MAX),
	    EMCodeTimeReasons	NVARCHAR(MAX),
	    EMCodeTimeNotes	NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def pat_2_staging_table(table_name="PAT_2_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PAT_2 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    return f"""
    CREATE TABLE {table_name}(
    	Patient_Number	NVARCHAR(MAX),
	    Last	NVARCHAR(MAX),
	    First	NVARCHAR(MAX),
	    M	NVARCHAR(MAX),
	    Birthdate	NVARCHAR(MAX),
	    Age	NVARCHAR(MAX),
	    Language	NVARCHAR(MAX),
	    Address	NVARCHAR(MAX),
	    Address_1	NVARCHAR(MAX),
	    City	NVARCHAR(MAX),
	    State	NVARCHAR(MAX),
	    Zip	NVARCHAR(MAX),
	    Phone	NVARCHAR(MAX),
	    AllowVM_Home	NVARCHAR(MAX),
	    Cell	NVARCHAR(MAX),
	    AllowVM_Cell	NVARCHAR(MAX),
	    AllowTextCell	NVARCHAR(MAX),
	    PromotionalTextOptIn	NVARCHAR(MAX),
	    SurveyOptIn	NVARCHAR(MAX),
	    PromotionalEmailOptIn	NVARCHAR(MAX),
	    SendPatientBalanceReminders	NVARCHAR(MAX),
	    Hear_From	NVARCHAR(MAX),
	    Last_Service_Date	NVARCHAR(MAX),
	    Ins_Name	NVARCHAR(MAX),
	    Ins_Address1	NVARCHAR(MAX),
	    Ins_Address2	NVARCHAR(MAX),
	    Ins_City	NVARCHAR(MAX),
	    Ins_State	NVARCHAR(MAX),
	    Ins_Zip	NVARCHAR(MAX),
	    Ins_Phone	NVARCHAR(MAX),
	    Race	NVARCHAR(MAX),
	    Ethnicity	NVARCHAR(MAX),
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def adj_4_staging_table(table_name="ADJ_4_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a ADJ_4 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    # TODO: textbox20: Rename the column
    return f"""
    CREATE TABLE {table_name}(
    	Inv_Num nvarchar(max),
	    textbox20 nvarchar(max),
	    Svc_Date nvarchar(max),
	    Clinic nvarchar(max),
	    Rev_Type nvarchar(max),
	    Trans_Date nvarchar(max),
	    Phy_Name nvarchar(max),
	    Proc_Code nvarchar(max),
	    Payer nvarchar(max),
	    Payer_Name nvarchar(max),
	    Adj_Amt float,
	    Reason nvarchar(max),
	    Crt_UserID nvarchar(max),
	    Client_ID int,
	    Date_Updated datetime
    );
    """


def pay_4_staging_table(table_name="PAY_4_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a PAY_4 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    # TODO: Rename textbox13 column
    return f"""
    CREATE TABLE {table_name}(
        Payer_Name NVARCHAR(MAX),
        textbox13 NVARCHAR(MAX),
        Inv_Num NVARCHAR(MAX),
        Trans_Date NVARCHAR(MAX),
        Proc_Code NVARCHAR(MAX),
        Payer NVARCHAR(MAX),
        Payment FLOAT,
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


def rev_16_staging_table(table_name="REV_16_Staging_Base"):
    """
    Generates a SQL `CREATE TABLE` statement for a REV_16 staging table.

    :param table_name: The name of the table to be created.
    :type table_name: str
    :returns: SQL table string.
    :rtype: str
    """
    # TODO: Rename textbox33 and textbox34 columns
    return f"""
    CREATE TABLE {table_name}(
        Clinic NVARCHAR(MAX),
        Rev_Type NVARCHAR(MAX),
        textbox33 NVARCHAR(MAX),
        textbox34 NVARCHAR(MAX),
        Visit NVARCHAR(MAX),
        Ref_Clinic NVARCHAR(MAX),
        Category NVARCHAR(MAX),
        inv_num NVARCHAR(MAX),
        PAT_NUM NVARCHAR(MAX),
        Last_name NVARCHAR(MAX),
        First_name NVARCHAR(MAX),
        Charge_Amt FLOAT,
        Rebilled_Amt FLOAT,
        Client_ID INT,
        Date_Updated DATETIME
    );
    """


if __name__ == "__main__":
    pass
    # TODO: Create all the table in the database if this file is called, if table exists print the message table already exists
