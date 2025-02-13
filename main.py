import time

from utils.selenium_driver import SeleniumDriver

browsers = ['chrome', 'firefox', 'edge']

for browser in browsers:
    selenium = SeleniumDriver(browser=browser)
    driver = selenium.setup_driver()
    driver.get("https://www.google.com")
    time.sleep(5)
    driver.quit()