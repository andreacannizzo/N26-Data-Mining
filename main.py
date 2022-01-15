from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


auto_chromedriver = chromedriver_autoinstaller.install()
browser = webdriver.Chrome(auto_chromedriver)
browser.get('https://app.n26.com/login')
login(browser, username, password)

# Commentato perchè in prova è troppo lungo
scroll_to_bottom(browser)

# "//li/" for web elements, "//li/div/p/span/span[1]/a" to obtain href of each element
# but the element whit the href is not clickable
URL_elements = browser.find_elements_by_xpath("//li/div/p/span/span[1]/a")
URL_lists = []
Data_Set = pd.DataFrame()
N_range = URL_elements.__len__()-1

for i in range(N_range):
    # print(i)
    URL_lists.append(URL_elements[i].get_attribute("href"))
    # open new tab, go there and load page
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(URL_lists[i])
    # retrieve data
    name = get_name(browser)  # string
    value = get_value(browser)  # float
    date = get_date(browser)  # datetime_object
    category = get_category(browser)  # string
    tags = get_tags(browser)  # string
    # create Data Frame
    line = pd.DataFrame({"Data": [date],
                         "Beneficiario": [name],
                         "Importo": [value],
                         "URL": [URL_lists[i]],
                         "Categoria": [category],
                         "Tags": [tags]})
    Data_Set = Data_Set.append(line, ignore_index=True)
    # close new tab and go back to main
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

Data_Set.to_csv('N26_Data.csv', index=False)
browser.close()
