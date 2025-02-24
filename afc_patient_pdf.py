import os

from dotenv import load_dotenv

load_dotenv()

from utils.pyodbc_sql import PyODBCSQL
from utils.selenium_driver import SeleniumDriver

DRIVER = "chrome"

sql = PyODBCSQL
slm = SeleniumDriver
driver = slm.setup_driver(DRIVER)
