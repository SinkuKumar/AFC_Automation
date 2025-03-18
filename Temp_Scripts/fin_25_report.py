import os
import logging
import traceback
from dotenv import load_dotenv
import utils.file_folder as file_operation
from utils.general import get_current_date, get_past_date
from utils.pyodbc_sql import PyODBCSQL
from utils.experity_base import ExperityBase, close_other_windows
from utils.selenium_driver import SeleniumDriver
from utils.extract_transform import fin_25_report_data_transformation

client_ids = [3671]
report_from_date = '01/01/2022'  # MM/DD/YYYY format
report_to_date =  '03/10/2025'   # MM/DD/YYYY format

# Use below If you want for particular number of days, months, years, quarters
# report_from_date = get_past_date(years=1)   # MM/DD/YYYY format
# report_to_date =  get_current_date()        # MM/DD/YYYY format

BROWSER = 'chrome'
DOWNLOAD_DIR = os.getcwd()
WINDOW_WIDTH, WINDOW_HEIGHT = None, None
EXPERITY_URL = 'https://pvpm.practicevelocity.com'
TABLE_NAME = 'Test_Auto_Staging_Fin_25'

current_dir = os.getcwd()
download_dir = os.path.join(os.path.dirname(current_dir), 'AFC_Test_Files')

selenium = SeleniumDriver(browser=BROWSER, download_directory=download_dir, window_width=WINDOW_WIDTH, window_height= WINDOW_HEIGHT)
driver = selenium.setup_driver()

load_dotenv()
DB = PyODBCSQL('BI_AFC')

def web_workflow():
    try:
        print(f'Web Workflow started for client : {client_id}')
        experity = ExperityBase(driver)
    
        experity.open_portal(EXPERITY_URL)
        experity.login(username, password)
        PORTAL_URL = experity.experity_version()
        experity.navigate_to(EXPERITY_URL, PORTAL_URL, "Reports")
        experity.search_and_select_report('FIN 25')
        experity.select_report_date_range(report_from_date, report_to_date)
        experity.select_logbook_status(['All'])
        experity.select_financial_class(['All'])
        experity.run_report()
        file_operation.clear_directory_files(download_dir)
        experity.download_report('CSV')
        file_operation.wait_for_download('FIN_25', download_dir)
        close_other_windows(driver)
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
        input_csv_file = os.path.join(download_dir, r"FIN_25_RealTimeChargesReview.csv")
        output_csv_file = os.path.join(download_dir, r"FIN_25_transformed_data.csv")
        fin_25_report_data_transformation(input_csv_file, output_csv_file, client_id)
        DB.csv_bulk_insert(output_csv_file, TABLE_NAME)
        print(f'Data transformation and Records insertion completed for client : {client_id}')
        logging.info('Database workflow completed!')
    except Exception as e:
        print(e)
        logging.error(f'An unexpected error occurred during the ETL process: {e}', exc_info=True)

user_credentials = DB.get_users_credentials(client_ids)
for client_id, username, password in user_credentials:
    status = False
    status = web_workflow()
    # if status:
    #     data_workflow()