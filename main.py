import os
import time
import logging
import traceback
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase
from dotenv import load_dotenv

BROWSER = 'chrome'
DOWNLOAD_DIR = os.getcwd()
WINDOW_WIDTH = None
WINDOW_HEIGHT = None
EXPERITY_URL = 'https://pvpm.practicevelocity.com'
PORTAL_URL = '25_1'

selenium = SeleniumDriver(browser=BROWSER, download_directory=DOWNLOAD_DIR, window_width=WINDOW_WIDTH, window_height= WINDOW_HEIGHT)
driver = selenium.setup_driver()

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

try:
    experity = ExperityBase(driver)
    experity.open_portal(EXPERITY_URL)
    experity.login(username, password)
    experity.navigate_to_sub_nav(EXPERITY_URL, PORTAL_URL, "Summary")
    experity.navigate_to_recievables_page(12345)
    time.sleep(2)

except Exception as e:
    logging.error("An unexpected error occured : \n" + traceback.format_exc())
    print(e)
finally:
    driver.quit()
    logging.info("Browser closed successfully.")