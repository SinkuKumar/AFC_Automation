import os
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from utils.pyodbc_sql import PyODBCSQL
from utils.selenium_driver import SeleniumDriver

# Load environment variables
load_dotenv()

# Constants
DRIVER = "chrome"
DOWNLOAD_DIRECTORY = "/Users/Sinku/Development/AFC_Automation/Downloads"
WAIT_TIME = 100
NUM_WORKERS = 5  # Number of concurrent Selenium workers

# SQL connection
sql = PyODBCSQL('BI_AFC')

def fetch_next_record():
    """Fetches the next available record that needs processing."""
    query = """
    SELECT TOP 1 ID, Client_id, P_Num, L_Num, Access_code 
    FROM MB_trans_master_progress 
    WHERE file_location IS NULL AND file_uploaddate IS NULL AND client_id = 16
    ORDER BY ID ASC
    """
    return sql.execute_query(query)

def update_status(record_id, file_location):
    """Updates the status of the downloaded PDF in the SQL table."""
    date_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_query = """
    UPDATE MB_trans_master_progress 
    SET file_location = '{}', file_uploaddate = '{}'
    WHERE ID = '{}'
    """
    # sql.execute_query(update_query.format(file_location, date_stamp, record_id))
    with open('results.txt', 'a') as file:
        file.write(f"Updated record {record_id} with {file_location}\n\t{update_query.format(file_location, date_stamp, record_id)}\n")
    print(f"Updated record {record_id} with {file_location}\n\t{update_query.format(file_location, date_stamp, record_id)}")


def wait_for_download(download_path):
    """Waits for the PDF file to appear in the download directory."""
    timeout = WAIT_TIME  # Max wait time in seconds
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if os.path.exists(download_path):
            return True
        time.sleep(2)
    
    return False

def process_record(record):
    """Processes a single record: fetch -> download -> update."""
    if not record:
        print("No records found.")
        return
    u_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
    record_id, client_id, p_num, l_num, access_code = record
    pdf_url = f"https://gmb.graphxsys.com/Home/PDF?a={access_code}&p={p_num}&c={client_id}&id={record_id}-{u_id}"
    
    # Setup Selenium driver
    slm = SeleniumDriver(DRIVER, DOWNLOAD_DIRECTORY)
    driver = slm.setup_driver()
    driver.implicitly_wait(WAIT_TIME)

    driver.get(pdf_url)
    
    download_path = os.path.join(DOWNLOAD_DIRECTORY, f"AFC-Medical-Billing-{record_id}-{u_id}.pdf")
    
    if wait_for_download(download_path):
        print(f"Download complete: {download_path}")
        update_status(record_id, download_path)
    else:
        print(f"Download failed for record {record_id}")

    driver.quit()

def main():
    """Main function to manage multiple workers for downloading PDFs."""
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        while True:
            record = fetch_next_record()
            if not record:
                print("No more records to process. Exiting...")
                break
            executor.submit(process_record, record[0])  # Process first result

if __name__ == "__main__":
    main()
