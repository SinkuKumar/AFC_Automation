import os
import argparse
from dotenv import load_dotenv
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase
from utils.pyodbc_sql import PyODBCSQL

# Load environment variables
load_dotenv()

# Constants
BROWSER = 'chrome'
DOWNLOAD_DIR = '/Downloads'
EXPERITY_URL = 'https://pvpm.practicevelocity.com'

# SQL Server Credentials
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

# SQL Docker Credentials
SQL_DOCKER_SERVER = os.getenv('SQL_DOCKER_SERVER')
SQL_DOCKER_DATABASE = os.getenv('SQL_DOCKER_DATABASE')
SQL_DOCKER_USERNAME = os.getenv('SQL_DOCKER_USERNAME')
SQL_DOCKER_PASSWORD = os.getenv('SQL_DOCKER_PASSWORD')

def get_clinic(client_id):
    # Initialize database connections
    sql_server = PyODBCSQL(SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD)
    sql_docker = PyODBCSQL(SQL_DOCKER_SERVER, SQL_DOCKER_DATABASE, SQL_DOCKER_USERNAME, SQL_DOCKER_PASSWORD)
    
    # Setup Selenium driver
    sel_driver = SeleniumDriver(BROWSER, DOWNLOAD_DIR)
    driver = sel_driver.setup_driver()
    experity = ExperityBase(driver)
    
    # Fetch credentials for the provided client_id
    query = f"SELECT TOP 1 * FROM afc_password_tbl WHERE active = 1 AND client_id LIKE '%{client_id}%'"
    credentials = sql_server.execute_query(query)
    
    if not credentials:
        print(f"No credentials found for client_id: {client_id}")
        return
    
    client_id, _, username, password, _ = credentials[0]
    
    # Perform Experity login and fetch clinic data
    experity.open_portal(EXPERITY_URL)
    experity.login(username, password)
    experity_version = experity.get_portal_url()
    experity.navigate_to(EXPERITY_URL, experity_version, 'Clinic')
    clinic = experity.get_clinic_list()
    
    # Append client_id to clinic data and insert into database
    clinic = [list(list(row) + [str(client_id)]) for row in clinic]
    clinic[0][-1] = 'Client_ID'
    sql_docker.insert_data(clinic, 'clinic')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Experity script with a specified client_id.")
    parser.add_argument("client_id", type=str, help="Client ID to fetch credentials for.")
    args = parser.parse_args()
    
    get_clinic(args.client_id)
