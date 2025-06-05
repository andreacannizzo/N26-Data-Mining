from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import locale
from datetime import datetime
import time
import pandas as pd
import logging


def login(browser, username_str: str, password_str: str) -> None:
    """Effettua il login su N26 con le credenziali fornite."""
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
            logging.info(f"You have {20-i} seconds to accept access")
            time.sleep(1)
    except Exception as e:
        logging.error(f"problem(s) while logging in: {e}")


def chiudi_ad(browser) -> None:
    """Chiude l'ad iniziale se presente."""
    try:
        chiudi = browser.find_element("xpath", "//*[contains(text(),'Chiudi')]")
        chiudi.submit()
    except Exception:
        logging.info("Initial ad not found and not closed")


def logout(browser) -> None:
    """Effettua il logout dall'account N26."""
    try:
        browser.get('https://app.n26.com/account')
        exit_logo = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@title='Disconnetti']")))
        exit_logo.send_keys(Keys.RETURN)
    except Exception as e:
        logging.warning(f"Logout failed: {e}")


def scroll_to_bottom(browser) -> None:
    """Scorre fino in fondo alla pagina, cliccando il bottone 'Carica di più' se presente."""
    try:
        button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
        while button.size != 0:
            try:
                button = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
            except Exception:
                logging.info("Sono arrivato alla fine")
            button.send_keys(Keys.RETURN)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception:
        logging.info("Sono già arrivato alla fine")


def scroll_to_bottom_times(browser, times: int) -> None:
    """Scorre verso il basso un numero specificato di volte."""
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        for i in range(times):
            load_more_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Carica di più')]]"))
            )
            load_more_button.click()
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except Exception:
        logging.info("Non trovo il tasto per scrollare in basso")


def get_tags(browser) -> str:
    """Estrae i tag dalla pagina corrente."""
    tags_lists = []
    jointed_tags = ""
    try:
        tags_elements = WebDriverWait(browser, 2).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='main']/div/div[*]/a[*]/div/span")))
        for i in range(tags_elements.__len__()):
            tags_lists.append(tags_elements[i].text)

        for element in tags_lists:
            jointed_tags = jointed_tags + element
        return jointed_tags
    except Exception:
        return jointed_tags


def get_name(browser) -> str:
    """Estrae il nome del beneficiario dalla pagina corrente."""
    name = ""
    logo = True
    try:
        logo_element = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b q']")))
    except Exception:
        logo = False
    try:
        if logo:
            name = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[1]/h1/p"))).text
        else:
            name = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[1]/h1/p"))).text
        return name
    except Exception:
        return name


def get_value(browser) -> float:
    """Estrae il valore della transazione dalla pagina corrente."""
    logo = True
    try:
        logo_element = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b q']")))
    except Exception:
        logo = False
    if logo:
        amount = WebDriverWait(browser, 5).until(#//*[@id="main"]/div/div[1]/div[2]/div/div[2]/section/div/div[1]/span
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[1]/span"))).text
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if '.' in amount:
            value = re.findall(r"[-+]?\d+\.\d+", amount)[0]
        else:
            value = re.findall(r"[-+]?\d+", amount)[0]
        value = float(value)
    else:
        amount = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[1]/span"))).text
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if '.' in amount:
            value = re.findall(r"[-+]?\d+\.\d+", amount)[0]
        else:
            value = re.findall(r"[-+]?\d+", amount)[0]
        value = float(value)
    return value


def get_date(browser) -> datetime:
    """Estrae la data della transazione dalla pagina corrente."""
    logo = True
    try:
        logo_element = WebDriverWait(browser, 2).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@class='b q']")))
    except Exception:
        logo = False
    if logo:
        date_str = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[2]/div/span/span/span"))).text
    else:
        date_str = WebDriverWait(browser, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[2]/div/span"))).text
    try:
        locale.setlocale(locale.LC_TIME, 'it_IT')
    except locale.Error:
        logging.warning("Locale 'it_IT' not available, using default locale.")
    date_str = date_str.split(sep=' ·', maxsplit=1)[0]
    try:
        datetime_object = datetime.strptime(date_str, '%A %d %B %Y, %H:%M')
    except Exception as e:
        logging.error(f"Date parsing failed: {e}")
        raise
    return datetime_object


def get_category(browser) -> str:
    """Estrae la categoria della transazione dalla pagina corrente."""
    category_element = WebDriverWait(browser, 1).until(
                        EC.visibility_of_all_elements_located((By.XPATH,
                        "//*[@id='main']/div/div[*]/div[2]/div/div[1]/div/div[2]/div/div/p[2]")))
    return category_element[0].text


def get_last_time(csv_name) -> str:
    """Estrae l'ultima data registrata nel file CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 0]


def get_last_url(csv_name) -> str:
    """Estrae l'ultimo URL registrato nel file CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 1]


def get_last_beneficiary(csv_name) -> str:
    """Estrae l'ultimo beneficiario registrato nel file CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 2]


def get_last_import(csv_name) -> float:
    """Estrae l'ultimo importo registrato nel file CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 3]


def get_NewTag_string(tags, label_csv_name) -> str:
    """Restituisce il nuovo tag associato alla transazione."""
    labels = pd.read_csv(label_csv_name, na_filter=False)
    labels_list = labels["label"].to_list()

    tags_in_Tags = tags.split('#')[1:]
    intersection = set(tags_in_Tags) & set(labels_list)
    if len(intersection) == 1:
        return list(intersection)[0]
    else:
        logging.warning("Problem with row, tag not found in labels or inherent problem")
        return 0


def mine(browser, label_csv_name, csv_target_name) -> pd.DataFrame:
    """Estrae e memorizza i dati delle transazioni nel file CSV di destinazione."""
    li_xpath = "//li[contains(@class, 'q1hbnko')]"
    url_elements = browser.find_elements(By.XPATH, li_xpath)
    i = 0
    url_elem = url_elements[i]
    title_parts = url_elem.find_elements(By.XPATH, ".//span[contains(@class, 'q1hbnk7s')]")
    name = title_parts[0].text
    browser.execute_script("window.open('');")
    url = url_elem.find_element(By.XPATH, ".//a[@data-testid='feed-timeline-item']").get_attribute("href")
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(0.5)
    browser.get(url)
    try:
        value = get_value(browser)  # float
        date = get_date(browser)  # datetime_object
        category = get_category(browser)  # string
        tags = get_tags(browser)  # string
        newtag = get_NewTag_string(tags, label_csv_name)
        logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
    except Exception as e:
        logging.error(f"Couldn't retrieve values from transaction's tab {url}: {e}")
        input("Press Enter to try again and continue...")
        value = get_value(browser)  # float
        date = get_date(browser)  # datetime_object
        category = get_category(browser)  # string
        tags = get_tags(browser)  # string
        newtag = get_NewTag_string(tags, label_csv_name)
        logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    last_time = get_last_time(csv_target_name)
    last_beneficiary = get_last_beneficiary(csv_target_name)
    last_import = get_last_import(csv_target_name)

    lines = pd.DataFrame({"Data": [],
                          "URL": [],
                          "Beneficiario": [],
                          "Importo": [],
                          "Categoria": [],
                          "Tags": [],
                          "NewTags": []})

    while (str(date) != last_time) or (name != last_beneficiary) or (value != last_import):
        line = pd.DataFrame({"Data": [date],
                             "URL": [url],
                             "Beneficiario": [name],
                             "Importo": [value],
                             "Categoria": [category],
                             "Tags": [tags],
                             "NewTags": [newtag]})
        lines = pd.concat([line, lines], ignore_index=True)
        i = i + 1
        if i == url_elements.__len__():
            scroll_to_bottom_times(browser, 1)
            url_elements = browser.find_elements(By.XPATH, li_xpath)
        url_elem = url_elements[i]
        title_parts = url_elem.find_elements(By.XPATH, ".//span[contains(@class, 'q1hbnk7s')]")
        name = title_parts[0].text
        browser.execute_script("window.open('');")
        url = url_elem.find_element(By.XPATH, ".//a[@data-testid='feed-timeline-item']").get_attribute("href")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        try:
            value = get_value(browser)  # float
            date = get_date(browser)  # datetime_object
            category = get_category(browser)  # string
            tags = get_tags(browser)  # string
            newtag = get_NewTag_string(tags, label_csv_name)
            logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
        except Exception as e:
            logging.error(f"Couldn't retrieve values from transaction's tab {url}: {e}")
            input("Press Enter to try again and continue...")
            value = get_value(browser)  # float
            date = get_date(browser)  # datetime_object
            category = get_category(browser)  # string
            tags = get_tags(browser)  # string
            newtag = get_NewTag_string(tags, label_csv_name)
            logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1.5)

    return lines


# def get_number_of_new_lines(browser):
#     url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
#     start = 0
#     stop = url_elements.__len__()
#     max = 5
#     while max > 0:
#         print(start, stop)
#         for i in range(start, stop):
#             if get_last_url("N26_Data.csv") == url_elements[i].get_attribute("href"):
#                 return i
#         scroll_to_bottom_times(browser, 1)
#         time.sleep(1)
#         start = stop - 1
#         url_elements = browser.find_elements(By.XPATH, "//li/div/p/span/span[1]/a")
#         stop = url_elements.__len__()
#         max = max - 1


def tests(browser, csv_name, csvline2check) -> bool:
    """Esegue i test di verifica sui dati estratti."""
    test_passed = True
    df = pd.read_csv(csv_name, na_filter=False)
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(df.iloc[csvline2check, 1])
    test_value = get_value(browser)
    test_date = get_date(browser)
    test_category = get_category(browser)
    test_tags = get_tags(browser)
    target_value = df.iloc[csvline2check, 3]
    target_date = df.iloc[csvline2check, 0]
    target_category = df.iloc[csvline2check, 4]
    target_tags = df.iloc[csvline2check, 5]
    if test_value != target_value:
        logging.error(f"problem with value test {target_date} transaction: test_value = {test_value} != target_value = {target_value}")
        test_passed = False
    # else:
    #     print(f"{target_date} -> test_value = {test_value} = target_value = {target_value} OK")
    if test_date.__str__() != target_date:
        logging.error(f"problem with date test {target_date} transaction: test_date = {test_date} != target_date = {target_date}")
        test_passed = False
    # else:
    #     print(f"{target_date} -> test_date = {test_date} = target_date = {target_date} OK")
    if test_category != target_category:
        logging.error(f"problem with category test {target_date} transaction: test_category = {test_category} != target_category = {target_category}")
        test_passed = False
    # else:
    #     print(f"{target_date} -> test_category = {test_category} = target_category = {target_category} OK")
    if test_tags != target_tags:
        logging.error(f"problem with tags test {target_date} transaction: test_tags = {test_tags} != target_tags = {target_tags}")
        test_passed = False
    # else:
    #     print(f"{target_date} -> test_tags = {test_tags} = target_tags = {target_tags} OK")
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return test_passed

