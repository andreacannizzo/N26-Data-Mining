from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd

# solve the certificate issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# download latest chromedriver and open a new browser window
auto_chromedriver = chromedriver_autoinstaller.install()
browser = webdriver.Chrome(auto_chromedriver)
# load n26 website and log in with inputs.py credentials
browser.get('https://app.n26.com/login')
login(browser, username, password)
# close initial N26 ad
chiudi_ad(browser)
# get new lines to register
new_lines = mine(browser)
# drop last temp line
new_lines = new_lines[:-1]
# write on .csv file
new_lines.to_csv('N26_Data.csv', index=False, header=False, mode='a')
logout(browser)
browser.close()
