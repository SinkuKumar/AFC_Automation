import os

from dotenv import load_dotenv

load_dotenv()

from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase

BROSWER = 'chrome'
DOWNLOAD_PATH = '/Downloads'
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
TIMEOUT = 100

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

EXPERITY_URL = 'https://pvpm.practicevelocity.com'
PORTAL_URL = '25_1'

sel_driver = SeleniumDriver(BROSWER, DOWNLOAD_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)
driver = sel_driver.setup_driver()

experity = ExperityBase(driver, TIMEOUT)

experity.open_portal(EXPERITY_URL)
experity.login(USERNAME, PASSWORD)
experity.navigate_to_sub_nav(EXPERITY_URL, PORTAL_URL, "Reports")
experity.search_and_select_report('CNT_27')

