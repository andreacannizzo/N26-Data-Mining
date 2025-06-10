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
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Costanti xPath e timeout
XPATH_CHIUDI_AD = "//*[contains(text(),'Chiudi')]"
XPATH_LOGO = "//*[@class='b q']"
XPATH_NAME_LOGO = "//*[@id='main']/div/div[1]/div[2]/div/div[1]/h1/p"
XPATH_NAME_NOLOGO = "//*[@id='main']/div/div[1]/div/div/div[1]/h1/p"
XPATH_VALUE_LOGO = "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[1]/span"
XPATH_VALUE_NOLOGO = "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[1]/span"
XPATH_DATE_LOGO = "//*[@id='main']/div/div[1]/div[2]/div/div[2]/section/div/div[2]/div/span/span/span"
XPATH_DATE_NOLOGO = "//*[@id='main']/div/div[1]/div/div/div[2]/section/div/div[2]/div/span"
XPATH_CATEGORY = "//*[@id='main']/div/div[*]/div[2]/div/div[1]/div/div[2]/div/div/p[2]"
XPATH_TAGS = "//*[@id='main']/div/div[*]/a[*]/div/span"
LI_XPATH = "//li[contains(@class, 'q1hbnko')]"
XPATH_FEED_ITEM = ".//a[@data-testid='feed-timeline-item']"
DEFAULT_TIMEOUT = 10

# setup logging (in caso venga importato senza main)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login(browser, username_str: str, password_str: str) -> None:
    """Effettua il login su N26 usando le credenziali fornite."""
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
            logging.info(f"Hai {20-i} secondi per accettare l'accesso 2FA")
            time.sleep(1)
    except (NoSuchElementException, WebDriverException) as e:
        logging.error(f"Problemi durante il login: {e}")

def chiudi_ad(browser) -> None:
    """Chiude l'ad iniziale se presente."""
    try:
        chiudi = browser.find_element("xpath", XPATH_CHIUDI_AD)
        chiudi.submit()
    except NoSuchElementException:
        logging.info("Ad iniziale non trovato e non chiuso.")
    except Exception as e:
        logging.warning(f"Errore durante la chiusura dell'ad: {e}")

def logout(browser) -> None:
    """Effettua il logout dall'account N26."""
    try:
        browser.get('https://app.n26.com/account')
        exit_logo = WebDriverWait(browser, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@title='Disconnetti']")))
        exit_logo.send_keys(Keys.RETURN)
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Errore durante il logout: {e}")

def scroll_to_bottom(browser) -> None:
    """Scorri fino in fondo alla pagina delle transazioni."""
    try:
        button = WebDriverWait(browser, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
        while button.size != 0:
            try:
                button = WebDriverWait(browser, DEFAULT_TIMEOUT).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/section/div[4]/button")))
            except TimeoutException:
                logging.info("Fine della lista raggiunta.")
                break
            button.send_keys(Keys.RETURN)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except TimeoutException:
        logging.info("Già alla fine della lista.")

def scroll_to_bottom_times(browser, times: int) -> None:
    """Scorri verso il basso un numero specifico di volte."""
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        for i in range(times):
            load_more_button = WebDriverWait(browser, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Carica di più')]]"))
            )
            load_more_button.click()
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except TimeoutException:
        logging.info("Tasto 'Carica di più' non trovato.")

def get_tags(browser) -> str:
    """Recupera i tag associati alla transazione."""
    tags_lists = []
    jointed_tags = ""
    try:
        tags_elements = WebDriverWait(browser, 2).until(
            EC.visibility_of_all_elements_located((By.XPATH, XPATH_TAGS)))
        for elem in tags_elements:
            tags_lists.append(elem.text)
        for element in tags_lists:
            jointed_tags += element
        return jointed_tags
    except TimeoutException:
        return jointed_tags

def get_name(browser) -> str:
    """Recupera il nome del beneficiario della transazione."""
    name = ""
    logo = True
    try:
        WebDriverWait(browser, 1).until(
            EC.visibility_of_element_located((By.XPATH, XPATH_LOGO)))
    except TimeoutException:
        logo = False
    try:
        if logo:
            name = WebDriverWait(browser, 1).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_NAME_LOGO))).text
        else:
            name = WebDriverWait(browser, 1).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_NAME_NOLOGO))).text
        return name
    except TimeoutException:
        return name

def get_value(browser) -> float:
    """Recupera il valore della transazione."""
    logo = True
    try:
        WebDriverWait(browser, 1).until(
            EC.visibility_of_element_located((By.XPATH, XPATH_LOGO)))
    except TimeoutException:
        logo = False
    try:
        if logo:
            amount = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_VALUE_LOGO))).text
        else:
            amount = WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_VALUE_NOLOGO))).text
        amount = amount.replace('.', '').replace(',', '.')
        if '.' in amount:
            value = re.findall("[-+]?\d+\.\d+", amount)[0]
        else:
            value = re.findall("[-+]?\d+", amount)[0]
        return float(value)
    except (TimeoutException, IndexError) as e:
        logging.error(f"Errore nel recupero del valore: {e}")
        return 0.0

def get_date(browser) -> datetime:
    """Recupera la data della transazione."""
    logo = True
    try:
        WebDriverWait(browser, 2).until(
            EC.visibility_of_element_located((By.XPATH, XPATH_LOGO)))
    except TimeoutException:
        logo = False
    try:
        if logo:
            date_str = WebDriverWait(browser, 1).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_DATE_LOGO))).text
        else:
            date_str = WebDriverWait(browser, 1).until(
                EC.visibility_of_element_located((By.XPATH, XPATH_DATE_NOLOGO))).text
        locale.setlocale(locale.LC_TIME, 'it_IT')
        date_str = date_str.split(sep=' ·', maxsplit=1)[0]
        datetime_object = datetime.strptime(date_str, '%A %d %B %Y, %H:%M')
        return datetime_object
    except (TimeoutException, ValueError) as e:
        logging.error(f"Errore nel recupero della data: {e}")
        return datetime.now()

def get_category(browser) -> str:
    """Recupera la categoria della transazione."""
    try:
        category_element = WebDriverWait(browser, 1).until(
            EC.visibility_of_all_elements_located((By.XPATH, XPATH_CATEGORY)))
        return category_element[0].text
    except TimeoutException:
        return ""

def get_last_time(csv_name: str) -> str:
    """Restituisce la data dell'ultima transazione nel CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 0]

def get_last_url(csv_name: str) -> str:
    """Restituisce l'URL dell'ultima transazione nel CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 1]

def get_last_beneficiary(csv_name: str) -> str:
    """Restituisce il beneficiario dell'ultima transazione nel CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 2]

def get_last_import(csv_name: str) -> str:
    """Restituisce l'importo dell'ultima transazione nel CSV."""
    df = pd.read_csv(csv_name, na_filter=False)
    return df.tail(1).iloc[0, 3]

def get_NewTag_string(tags: str, label_csv_name: str) -> str:
    """Restituisce il nuovo tag associato ai tags trovati."""
    labels = pd.read_csv(label_csv_name, na_filter=False)
    labels_list = labels["label"].to_list()
    tags_in_Tags = tags.split('#')[1:]
    intersection = set(tags_in_Tags) & set(labels_list)
    if len(intersection) == 1:
        return list(intersection)[0]
    else:
        logging.warning("Tag non trovato in labels o problema inerente la riga.")
        return ""

def mine(browser, label_csv_name: str, csv_target_name: str) -> pd.DataFrame:
    """Estrae nuove transazioni e le restituisce come DataFrame."""
    try:
        url_elements = browser.find_elements(By.XPATH, LI_XPATH)
        i = 0
        url_elem = url_elements[i]
        title_parts = url_elem.find_elements(By.XPATH, ".//span[contains(@class, 'q1hbnk7s')]")
        name = title_parts[0].text
        browser.execute_script("window.open('');")
        url = url_elem.find_element(By.XPATH, XPATH_FEED_ITEM).get_attribute("href")
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(0.5)
        value = get_value(browser)
        date = get_date(browser)
        category = get_category(browser)
        tags = get_tags(browser)
        newtag = get_NewTag_string(tags, label_csv_name)
        logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        last_time = get_last_time(csv_target_name)
        last_beneficiary = get_last_beneficiary(csv_target_name)
        last_import = get_last_import(csv_target_name)
        lines = pd.DataFrame({"Data": [], "URL": [], "Beneficiario": [], "Importo": [], "Categoria": [], "Tags": [], "NewTags": []})
        while (str(date) != last_time) or (name != last_beneficiary) or (value != last_import):
            line = pd.DataFrame({"Data": [date], "URL": [url], "Beneficiario": [name], "Importo": [value], "Categoria": [category], "Tags": [tags], "NewTags": [newtag]})
            lines = pd.concat([line, lines], ignore_index=True)
            i += 1
            if i == len(url_elements):
                scroll_to_bottom_times(browser, 1)
                url_elements = browser.find_elements(By.XPATH, LI_XPATH)
            url_elem = url_elements[i]
            title_parts = url_elem.find_elements(By.XPATH, ".//span[contains(@class, 'q1hbnk7s')]")
            name = title_parts[0].text
            browser.execute_script("window.open('');")
            url = url_elem.find_element(By.XPATH, XPATH_FEED_ITEM).get_attribute("href")
            browser.switch_to.window(browser.window_handles[1])
            value = get_value(browser)
            date = get_date(browser)
            category = get_category(browser)
            tags = get_tags(browser)
            newtag = get_NewTag_string(tags, label_csv_name)
            logging.info(f"{i} {date} {name} {value} {category} {tags} {newtag}")
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(1.5)
        return lines
    except Exception as e:
        logging.error(f"Errore durante il mining delle transazioni: {e}")
        return pd.DataFrame()

def tests(browser, csv_name: str, csvline2check: int) -> bool:
    """Esegue test di coerenza su una riga del CSV."""
    test_passed = True
    df = pd.read_csv(csv_name, na_filter=False)
    try:
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
            logging.warning(f"Problema con il test valore {target_date}: test_value = {test_value} != target_value = {target_value}")
            test_passed = False
        if str(test_date) != target_date:
            logging.warning(f"Problema con il test data {target_date}: test_date = {test_date} != target_date = {target_date}")
            test_passed = False
        if test_category != target_category:
            logging.warning(f"Problema con il test categoria {target_date}: test_category = {test_category} != target_category = {target_category}")
            test_passed = False
        if test_tags != target_tags:
            logging.warning(f"Problema con il test tags {target_date}: test_tags = {test_tags} != target_tags = {target_tags}")
            test_passed = False
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except Exception as e:
        logging.error(f"Errore durante il test della riga {csvline2check}: {e}")
        try:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        except Exception:
            pass
        return False
    return test_passed

