import os
from utils.selenium_driver import SeleniumDriver
from utils.experity_base import ExperityBase

BROWSER = 'chrome'
DOWNLOAD_DIR = os.getcwd()

selenium = SeleniumDriver(browser=BROWSER, download_directory=DOWNLOAD_DIR)
driver = selenium.setup_driver()

ExperityBase(driver)



"""
import time

from utils.selenium_driver import SeleniumDriver

browsers = ['chrome', 'firefox', 'edge']

for browser in browsers:
    selenium = SeleniumDriver(browser=browser)
    driver = selenium.setup_driver()
    driver.get("https://www.google.com")
    time.sleep(5)
    driver.quit()

# print(0/0)

raise Exception("Message: This is an error | Error Code: 1xxx | Contact Automation Team L1 or above.")
"""
