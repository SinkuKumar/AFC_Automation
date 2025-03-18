import os
import logging
import traceback
from datetime import datetime
from dotenv import load_dotenv
import utils.file_folder as file_operation
from utils.pyodbc_sql import PyODBCSQL
from utils.experity_base import ExperityBase, close_other_windows, run_logic_for_each_month
from utils.selenium_driver import SeleniumDriver
from utils.extract_transform import combine_csv_files, rev_19_report_data_transformation
from utils.create_table_queries import rev_19_create_query

load_dotenv()
# db = PyODBCSQL('BI_AFC')

# client_ids = db.get_all_active_client_ids()   # For all clients
client_ids = [2001]                             # For particular clients 
report_from_month = 'June 2024'                 # Month Year format (e.g., 'March 2010')
report_to_month = 'February 2025'               # Month Year format (e.g., 'March 2010')

REPORT_NAME = 'REV_19'
BROWSER = 'chrome'
ALL_FILES_DIR = os.path.join(os.getcwd(), 'Downloads', 'Rev_19')
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'Downloads', 'Rev_19_TEMP')
WINDOW_WIDTH, WINDOW_HEIGHT = None, None
EXPERITY_URL = 'https://pvpm.practicevelocity.com'

date_folder = rf'{ALL_FILES_DIR}\{datetime.now().strftime("%m-%d-%Y")}'
file_operation.create_directories([date_folder, DOWNLOAD_DIR])

logging.info(f"{'-'*30}")
logging.info('  New Automation run started')
logging.info(f"{'-'*30}")
selenium = SeleniumDriver(browser=BROWSER, download_directory=DOWNLOAD_DIR, window_width=WINDOW_WIDTH, window_height= WINDOW_HEIGHT)

l_username = os.getenv('USERNAME')
l_password = os.getenv('PASSWORD')

def web_workflow():
    try:
        print(f'Web Workflow started for client : {client_id}')
        driver = selenium.setup_driver()
        experity = ExperityBase(driver, 300)

        def rev_19_report_steps(month_name):
            experity.select_month(month = month_name)
            experity.run_report()
            experity.download_report('CSV')
            file_operation.wait_for_download(REPORT_NAME, DOWNLOAD_DIR)
            old_file_name = os.path.join(DOWNLOAD_DIR, 'REV_19_TotalRevenueByProviderAndCategory.csv')
            new_file_name = os.path.join(DOWNLOAD_DIR, f'REV_19_{month_name}.csv')
            file_operation.rename_file_or_folder(old_file_name, new_file_name)
            close_other_windows(driver)

        experity.open_portal(EXPERITY_URL)
        experity.login(username, password)
        PORTAL_URL = experity.experity_version()
        experity.navigate_to(EXPERITY_URL, PORTAL_URL, "Reports")
        experity.search_and_select_report(REPORT_NAME)
        run_logic_for_each_month(report_from_month, report_to_month, rev_19_report_steps)
        combine_csv_files(DOWNLOAD_DIR, combined_csv_file_path, REPORT_NAME)
        experity.logout()
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
        # db.check_and_create_table(TABLE_NAME, rev_19_create_query(TABLE_NAME))
        # table_columns = db.get_column_names(TABLE_NAME)
        table_columns = [("Phy_Name",), ("Rev_Type",), ("Proc_Code",), ("Description", ), ("Charge_Amt", ), ("Client_id", ), ("Date_Updated", )]
        rev_19_report_data_transformation(combined_csv_file_path, transformed_csv_file_path, table_columns, client_id)
        # db.truncate_table(TABLE_NAME)
        # db.csv_bulk_insert(output_csv_file, TABLE_NAME)
        file_operation.move_paths([combined_csv_file_path, transformed_csv_file_path], date_folder)
        print(f'Data transformation and Records insertion completed for client : {client_id}')
        logging.info('Database workflow completed!')
    except Exception as e:
        print(e)
        logging.error(f'An unexpected error occurred during the ETL process: {e}', exc_info=True)

print('New Automation Run Started...\n')
# user_credentials = db.get_users_credentials(client_ids)
user_credentials = [(2001, l_username, l_password)]

for client_id, username, password in user_credentials:
    file_operation.clear_directory_files(DOWNLOAD_DIR)

    TABLE_NAME = f'REV_19_Staging_{client_id}'
    time_stamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    combined_csv_file_name = f'{REPORT_NAME}_{client_id}_{report_from_month.replace(" ", "-")}_{report_to_month.replace(" ", "-")}_{time_stamp}.csv'
    combined_csv_file_path = os.path.join(DOWNLOAD_DIR, combined_csv_file_name)
    transformed_csv_file_name = f'{REPORT_NAME}_{client_id}_{report_from_month.replace(" ", "-")}_{report_from_month.replace(" ", "-")}_{time_stamp}_transformed.csv'
    transformed_csv_file_path = os.path.join(DOWNLOAD_DIR, transformed_csv_file_name)
    status = False

    status = web_workflow()
    if status:
        data_workflow()
logging.info('Automation run Finished. Please review the results.')
print('\nAutomation run Finished. Please review the results.')