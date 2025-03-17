import os
import logging
import traceback
from dotenv import load_dotenv
import utils.file_folder as file_operation
from utils.general import get_yesterdays_date
from utils.pyodbc_sql import PyODBCSQL
from utils.experity_base import ExperityBase, close_other_windows
from utils.selenium_driver import SeleniumDriver
from utils.extract_transform import pay_10_report_data_transformation
from utils.create_table_queries import pay_10_create_query
from datetime import datetime

load_dotenv()
db = PyODBCSQL()

client_ids = db.get_all_active_client_ids()   # For all clients
# client_ids = [3671, 3681, 16]               # For particular clients
report_from_date = '01/01/2022'               # MM/DD/YYYY format
report_to_date =  get_yesterdays_date()       # MM/DD/YYYY format

REPORT_NAME = 'PAY_10'
BROWSER = 'chrome'
ALL_FILES_DIR = os.path.join(os.getcwd(), 'Downloads', 'Pay_10')
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'Downloads', 'Pay_10_TEMP')
WINDOW_WIDTH, WINDOW_HEIGHT = None, None
EXPERITY_URL = 'https://pvpm.practicevelocity.com'

date_folder = rf'{ALL_FILES_DIR}\{datetime.now().strftime("%m-%d-%Y")}'
file_operation.create_directories([date_folder, DOWNLOAD_DIR])

logging.info(f"{'-'*30}")
logging.info('  New Automation run started')
logging.info(f"{'-'*30}")
selenium = SeleniumDriver(browser=BROWSER, download_directory=DOWNLOAD_DIR, window_width=WINDOW_WIDTH, window_height= WINDOW_HEIGHT)

def web_workflow():
    try:
        print(f'Web Workflow started for client : {client_id}')
        driver = selenium.setup_driver()
        experity = ExperityBase(driver, 300)
        experity.open_portal(EXPERITY_URL)
        experity.login(username, password)
        PORTAL_URL = experity.experity_version()
        experity.navigate_to(EXPERITY_URL, PORTAL_URL, "Reports")
        experity.search_and_select_report(REPORT_NAME)
        experity.select_report_date_range(report_from_date, report_to_date)
        experity.run_report()
        experity.download_report('CSV')
        file_operation.wait_for_download(REPORT_NAME, DOWNLOAD_DIR, 500)
        close_other_windows(driver)
        experity.logout()

        file_operation.rename_file_or_folder(os.path.join(DOWNLOAD_DIR, download_csv_file_name), os.path.join(DOWNLOAD_DIR, download_csv_file_rename))
        print(f'Web Workflow completed successfully for client : {client_id}')
        return True
    except Exception as e:
        logging.error("An unexpected error occured : \n" + traceback.format_exc())
        print(e)
    finally:
        driver.quit()
        logging.info("Browser closed successfully.")

def data_workflow():
    logging.info("Database workflow started...")
    try:
        print(f'Data transformation and Records insertion process started for client : {client_id}')
        input_csv_file = os.path.join(DOWNLOAD_DIR, download_csv_file_rename)
        output_csv_file = os.path.join(DOWNLOAD_DIR, transformed_csv_file_name)
        db.check_and_create_table(TABLE_NAME, pay_10_create_query(TABLE_NAME))
        table_columns = db.get_column_names(TABLE_NAME)
        pay_10_report_data_transformation(input_csv_file, output_csv_file, table_columns, client_id)
        db.truncate_table(TABLE_NAME)
        db.csv_bulk_insert(output_csv_file, TABLE_NAME)
        file_operation.move_files_only(DOWNLOAD_DIR, date_folder)
        print(f'Data transformation and Records insertion completed for client : {client_id}')
        logging.info('Database workflow completed!')
    except Exception as e:
        print(e)
        logging.error(f'An unexpected error occurred during the ETL process: {e}', exc_info=True)

print('New Automation Run Started...\n')
user_credentials = db.get_users_credentials(client_ids)

for client_id, username, password in user_credentials:
    TABLE_NAME = f'PAY_10_Staging_{client_id}'
    file_operation.clear_directory_files(DOWNLOAD_DIR)
    time_stamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    download_csv_file_name ='PAY_10_PayerPatientPaidAdjustedByPayerClass.csv'
    download_csv_file_rename = f'{REPORT_NAME}_{client_id}_{report_from_date.replace("/", "-")}_{report_to_date.replace("/", "-")}_{time_stamp}.csv'
    transformed_csv_file_name = f'{REPORT_NAME}_{client_id}_{report_from_date.replace("/", "-")}_{report_to_date.replace("/", "-")}_{time_stamp}_transformed.csv'
    status = False
    status = web_workflow()
    if status:
        data_workflow()
        current_date = datetime.today().strftime('%Y/%m/%d')
        for i in range(1,7):
            query = f"exec [Py_AFC_Pay_10] {client_id},'Pay_10',{i},'{current_date}'"
            db.execute_query(query)
logging.info('Automation run Finished. Please review the results.')
print('\nAutomation run Finished. Please review the results.')