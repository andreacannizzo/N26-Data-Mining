from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
import os
import logging

# config
csv_target_name = os.getenv('CSV_TARGET_NAME', 'N26_History_With_Tags.csv')
label_csv_name = os.getenv('LABEL_CSV_NAME', 'labels.csv')

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# solve the certificate issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    """Main workflow for N26 data mining bot."""
    # download latest chromedriver and open a new browser window
    auto_chromedriver = chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    service = Service(executable_path=auto_chromedriver)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    try:
        browser.get('https://app.n26.com/login')
        login(browser, username, password)
        chiudi_ad(browser)
        browser.get('https://app.n26.com/feed/transactions')
        temp = pd.read_csv(csv_target_name, na_filter=False)
        last_row_of_df = temp.shape[0]-1
        try:
            for idx in [2695, 2699, 2690, 2600, 1992]:
                if not tests(browser, csv_target_name, idx):
                    logging.error(f"Test failed at row {idx}")
                    return
        except Exception as e:
            logging.error(f"ALERT ----> tests failed, can not proceed with data mining <---- {e}")
            return
        new_lines = mine(browser, label_csv_name, csv_target_name)
        if len(new_lines) > 0:
            new_lines.to_csv(csv_target_name, index=False, header=False, mode='a')
    except Exception as e:
        logging.exception(f"Fatal error in main workflow: {e}")
    finally:
        try:
            logout(browser)
        except Exception as e:
            logging.warning(f"Error during logout: {e}")
        browser.close()

if __name__ == "__main__":
    main()
