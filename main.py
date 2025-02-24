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
    experity.navigate_to_sub_nav(EXPERITY_URL, PORTAL_URL, "Reports")
    # experity.navigate_to_recievables_page(12345)
    experity.search_and_select_report('CNT 27')
    experity.select_report_date_range('12/01/2024', '12/30/2024')
    experity.select_logbook_status(['All'])
    experity.select_financial_class(['All'])
    experity.select_arrival_status(['All'])
    experity.run_report()

    time.sleep(4)
    experity.switch_to_report_window()
    time.sleep(10)

    main_window = [handle for handle in driver.window_handles][0]
    logging.info(f"Switching to new window")
    driver.switch_to.window(main_window)

    time.sleep(2)
    experity.logout()
    time.sleep(3)

except Exception as e:
    logging.error("An unexpected error occured : \n" + traceback.format_exc())
    print(e)
finally:
    driver.quit()
    logging.info("Browser closed successfully.")