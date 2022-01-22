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
# N_range is the position of the last transaction registered in the .csv file
N_range = get_number_of_new_lines(browser)
# get the list of all transaction currently displayed in the browser
url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")

# it will register 100 new transaction at maximum
if N_range > 100:
    end = N_range - 100
else:
    end = -1

# register new data starting from the oldest to the newest
for i in range(N_range-1, end, -1):
    # open new tab, switch to new tab and load page
    browser.execute_script("window.open('');")
    url = url_elements[i].get_attribute("href")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(url)
    # extract data
    name = get_name(browser)  # string
    value = get_value(browser)  # float
    date = get_date(browser)  # datetime_object
    category = get_category(browser)  # string
    tags = get_tags(browser)  # string
    # create new row with Data Frame
    line = pd.DataFrame({"Data": [date],
                         "URL": [url],
                         "Beneficiario": [name],
                         "Importo": [value],
                         "Categoria": [category],
                         "Tags": [tags]})
    # add new row to .csv file (the csv files need to always end with a new blank line)
    line.to_csv('N26_Data.csv', index=False, header=False, mode='a')
    # close new tab and go back to home page
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)

logout(browser)
browser.close()
