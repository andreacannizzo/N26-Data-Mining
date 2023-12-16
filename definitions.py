from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import locale
from datetime import datetime
import time
import pandas as pd


def login(browser, username_str, password_str):
    try:
        username = browser.find_element("name", "username")
        username.clear()
        username.send_keys(username_str)
        password = browser.find_element("name", "password")
        password.clear()
        password.send_keys(password_str)
        submit = browser.find_element("xpath", "//button")
        submit.submit()
        for i in range(20):
            print(f"You have {20-i} seconds to accept access")
            time.sleep(1)
    except:
        print("problem(s) while logging in")


def logout(browser):
    browser.get('https://app.n26.com/account')
    exit_logo = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@title='Disconnetti']")))
    exit_logo.send_keys(Keys.RETURN)


def scroll_to_bottom(browser):
    try:
        button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
        while button.size != 0:
            try:
                button = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
            except:
                print("Sono arrivato alla fine")
            button.send_keys(Keys.RETURN)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        print("Sono già arrivato alla fine")


def scroll_to_bottom_times(browser, times):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        for i in range(times):
            button = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[3]/button")))
            button.click()
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except:
        print("Non trovo il tasto per scrollare in basso")


def get_tags(browser):
    tags_lists = []
    jointed_tags = ""
    try:
        tags_elements = WebDriverWait(browser, 2).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='main']/div/div[*]/div[*]/a/span/div/span")))
        for i in range(tags_elements.__len__()):
            tags_lists.append(tags_elements[i].text)

        for element in tags_lists:
            jointed_tags = jointed_tags + element
        return jointed_tags
    except:
        return jointed_tags


def get_name(browser):
    name = ""
    logo = True
    try:
        logo_element = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b e']")))
    except:
        logo = False
    try:
        if logo:
            name = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[1]/h1/p"))).text
        else:
            name = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[1]/h1/p"))).text
        return name
    except:
        return name


def get_value(browser):
    logo = True
    try:
        logo_element = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b e']")))
    except:
        logo = False
    if logo:
        amount = WebDriverWait(browser, 5).until(#//*[@id="main"]/div/div[1]/div[2]/div/div[2]/section/div/div[1]/span
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[1]/span"))).text
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if '.' in amount:
            value = re.findall("[-+]?\d+\.\d+", amount)[0]
        else:
            value = re.findall("[-+]?\d+", amount)[0]
        value = float(value)
    else:
        amount = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[1]/span"))).text
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if '.' in amount:
            value = re.findall("[-+]?\d+\.\d+", amount)[0]
        else:
            value = re.findall("[-+]?\d+", amount)[0]
        value = float(value)
    return value


def get_date(browser):
    logo = True
    try:
        logo_element = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b e']")))
    except:
        logo = False
    if logo:
        date_str = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[2]/span"))).text
    else:
        date_str = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[2]/span"))).text
    locale.setlocale(locale.LC_TIME, 'it_IT')
    date_str = date_str.split(sep=' ·', maxsplit=1)[0]
    datetime_object = datetime.strptime(date_str, '%A %d %B %Y, %H:%M')
    return datetime_object


def get_category(browser):
    category_element = WebDriverWait(browser, 1).until(
                        EC.visibility_of_all_elements_located((By.XPATH,
                        "//*[@id='main']/div/div[*]/div[2]/div/div[1]/div/div[2]/div/div/p[2]")))
    return category_element[0].text


def get_last_time(csv_name):
    df = pd.read_csv(csv_name)
    return df.tail(1).iloc[0, 0]


def get_last_url(csv_name):
    df = pd.read_csv(csv_name)
    return df.tail(1).iloc[0, 1]


def get_last_beneficiary(csv_name):
    df = pd.read_csv(csv_name)
    return df.tail(1).iloc[0, 2]


def get_last_import(csv_name):
    df = pd.read_csv(csv_name)
    return df.tail(1).iloc[0, 3]


def mine(browser):
    url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
    i = 0
    name = url_elements[i].text
    browser.execute_script("window.open('');")
    url = url_elements[i].get_attribute("href")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(url)
    value = get_value(browser)  # float
    date = get_date(browser)  # datetime_object
    category = get_category(browser)  # string
    tags = get_tags(browser)  # string
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    last_time = get_last_time('N26_Data.csv')
    last_beneficiary = get_last_beneficiary('N26_Data.csv')
    last_import = get_last_import('N26_Data.csv')

    lines = pd.DataFrame({"Data": [last_time],
                         "URL": [url],
                         "Beneficiario": [last_beneficiary],
                         "Importo": [last_import],
                         "Categoria": ["category"],
                         "Tags": ["tags"]})

    while (str(date) != last_time) or (name != last_beneficiary) or (value != last_import):
        line = pd.DataFrame({"Data": [date],
                             "URL": [url],
                             "Beneficiario": [name],
                             "Importo": [value],
                             "Categoria": [category],
                             "Tags": [tags]})
        lines = pd.concat([line, lines], ignore_index=True)
        i = i + 1
        if i == url_elements.__len__():
            scroll_to_bottom_times(browser, 1)
            url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
        name = url_elements[i].text
        browser.execute_script("window.open('');")
        url = url_elements[i].get_attribute("href")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        value = get_value(browser)  # float
        date = get_date(browser)  # datetime_object
        category = get_category(browser)  # string
        tags = get_tags(browser)  # string
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1.5)

    return lines


def get_number_of_new_lines(browser):
    url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
    start = 0
    stop = url_elements.__len__()
    max = 5
    while max > 0:
        print(start, stop)
        for i in range(start, stop):
            if get_last_url("N26_Data.csv") == url_elements[i].get_attribute("href"):
                return i
        scroll_to_bottom_times(browser, 1)
        time.sleep(1)
        start = stop - 1
        url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
        stop = url_elements.__len__()
        max = max - 1
