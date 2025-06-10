from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
import argparse
import logging
import os

# config
parser = argparse.ArgumentParser(description="N26 Data Mining Bot")
parser.add_argument('--csv_target_name', type=str, default="N26_History_With_Tags.csv", help="Nome file CSV target")
parser.add_argument('--label_csv_name', type=str, default="labels.csv", help="Nome file CSV etichette")
args = parser.parse_args()
csv_target_name = args.csv_target_name
label_csv_name = args.label_csv_name

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# solve the certificate issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def setup_browser():
    auto_chromedriver = chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    service = Service(executable_path=auto_chromedriver)
    return webdriver.Chrome(service=service, options=chrome_options)

def run_bot():
    if not os.path.exists(csv_target_name):
        logging.error(f"File CSV target '{csv_target_name}' non trovato.")
        return
    try:
        browser = setup_browser()
        browser.get('https://app.n26.com/login')
        login(browser, username, password)
        chiudi_ad(browser)
        browser.get('https://app.n26.com/feed/transactions')
        temp = pd.read_csv(csv_target_name, na_filter=False)
        last_row_of_df = temp.shape[0]-1
        try:
            for idx in [2695, 2699, 2690, 2600, 1992]:
                if not tests(browser, csv_target_name, idx):
                    logging.error(f"Test fallito alla riga {idx}.")
                    return
        except Exception as e:
            logging.error(f"ALERT ----> tests failed, cannot proceed with data mining <---- {e}")
            return
        new_lines = mine(browser, label_csv_name, csv_target_name)
        if len(new_lines) > 0:
            new_lines.to_csv(csv_target_name, index=False, header=False, mode='a')
        logout(browser)
    except Exception as e:
        logging.exception(f"Errore durante l'esecuzione del bot: {e}")
    finally:
        try:
            browser.close()
        except Exception:
            pass

if __name__ == "__main__":
    run_bot()
