from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service

# config
csv_target_name = "N26_History_With_Tags.csv"
label_csv_name = "labels.csv"

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
temp = pd.read_csv(csv_target_name, na_filter=False)
last_row_of_df = temp.shape[0]-1
try:
    if not tests(browser, csv_target_name, 2695):
        exit()
    if not tests(browser, csv_target_name, 2699):
        exit()
    if not tests(browser, csv_target_name, 2690):
        exit()
    if not tests(browser, csv_target_name, 2600):
        exit()
    if not tests(browser, csv_target_name, 1992):
        exit()
    if not tests(browser, csv_target_name, last_row_of_df):
        exit()
except:
    print("\nALERT ----> tests failed, can not proceed with data mining <----")
# get new lines to register
new_lines = mine(browser, label_csv_name, csv_target_name)
# write on .csv file only if there are new lines
if new_lines.__len__() > 0:
    new_lines.to_csv(csv_target_name, index=False, header=False, mode='a')
logout(browser)
browser.close()
