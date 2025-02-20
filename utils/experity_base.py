import time
import logging
from selenium import webdriver

class ExperityBase:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = None # Implement wait here
        self.webdriver.get("https://www.facebook.com")
        time.sleep(1000)

    def open_portal(self, url):
        self.webdriver.get()
