from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service

# solve the certificate issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# download latest chromedriver and open a new browser window
auto_chromedriver = chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=auto_chromedriver)
browser = webdriver.Chrome(service=service, options=chrome_options)
# load n26 website and log in with inputs.py credentials
browser.get('https://app.n26.com/login')
login(browser, username, password)
# close initial N26 ad
chiudi_ad(browser)
# run tests to see if bot is updated to current website version and xPaths
try:
    if not tests(browser, 'N26_Data.csv', 2695):
        exit()
    if not tests(browser, 'N26_Data.csv', 2699):
        exit()
    if not tests(browser, 'N26_Data.csv', 2690):
        exit()
    if not tests(browser, 'N26_Data.csv', 2600):
        exit()
    if not tests(browser, 'N26_Data.csv', 1992):
        exit()
except:
    print("\nALERT ----> tests failed, can not proceed with data mining <----")
# get new lines to register
new_lines = mine(browser)
# drop last temp line
new_lines = new_lines[:-1]
# write on .csv file only if there are new lines
if new_lines.__len__() > 0:
    new_lines.to_csv('N26_Data.csv', index=False, header=False, mode='a')
logout(browser)
browser.close()
