from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# create browser
auto_chromedriver = chromedriver_autoinstaller.install()
browser = webdriver.Chrome(auto_chromedriver)
# load n26 website and log in with inputs.py credentials
browser.get('https://app.n26.com/login')
login(browser, username, password)

# "//li/" for web elements, "//li/div/p/span/span[1]/a" to obtain href of each element
# but the element whit the href is not clickable

N_range = get_number_of_new_lines(browser)
url_elements = browser.find_elements_by_xpath("//li/div/p/span/span[1]/a")

if N_range > 500:
    end = N_range - 500
else:
    end = -1

for i in range(N_range-1, end, -1):
    # open new tab, go there and load page
    browser.execute_script("window.open('');")
    url = url_elements[i].get_attribute("href")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(url)
    # retrieve data
    name = get_name(browser)  # string
    value = get_value(browser)  # float
    date = get_date(browser)  # datetime_object
    category = get_category(browser)  # string
    tags = get_tags(browser)  # string
    # create Data Frame
    line = pd.DataFrame({"Data": [date],
                         "URL": [url],
                         "Beneficiario": [name],
                         "Importo": [value],
                         "Categoria": [category],
                         "Tags": [tags]})
    # with open('N26_Data.csv', mode='a') as f:
    #     f.write('\n')
    line.to_csv('N26_Data.csv', index=False, header=False, mode='a')
    # close new tab and go back to home page
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)

# browser.close()
