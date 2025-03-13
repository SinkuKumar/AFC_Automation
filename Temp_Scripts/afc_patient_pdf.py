import os
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from utils.pyodbc_sql import PyODBCSQL
from utils.selenium_driver import SeleniumDriver

DRIVER = "chrome"
DOWNLOAD_DIRECTORY = "/Users/Sinku/Development/AFC_Automation/Downloads"
WAIT_TIME = 100

sql = PyODBCSQL()

query = "SELECT TOP 1 ID, Client_id, P_Num, L_Num, Access_code FROM MB_trans_master_progress WHERE file_location IS NULL AND file_uploaddate IS NULL AND client_id = 16"
result = sql.execute_query(query)

def update_status(file_location):
    """
    Updates the status of the downloaded pdf file in sql table.
    Remember call this only once.
    """
    date_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_query = "UPDATE MB_trans_master_progress SET file_location = '{file_location}' AND file_uploaddate = '{date_stamp}'"


if result:
    slm = SeleniumDriver(DRIVER, DOWNLOAD_DIRECTORY)
    driver = slm.setup_driver()
    driver.implicitly_wait(WAIT_TIME)
    id, client_id, p_num, l_num, access_code = result[0]
    pdf_url = f"https://gmb.graphxsys.com/Home/PDF?a={access_code}&p={p_num}&c={client_id}"
    driver.get(pdf_url)
    update_status()

