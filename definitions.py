from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(browser, username_str, password_str):
    try:
        username = browser.find_element_by_name('username')
        username.clear()
        username.send_keys(username_str)
        password = browser.find_element_by_name('password')
        password.clear()
        password.send_keys(password_str)
        submit = browser.find_element_by_xpath("//button")
        submit.submit()
    except:
        print("problem(s) while logging in")


def scroll_to_bottom(browser):
    try:
        button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@title='Successivo']")))
        while button.size != 0:
            try:
                button = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@title='Successivo']")))
            except:
                print("Sono arrivato alla fine")
            button.send_keys(Keys.RETURN)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        print("Sono già arrivato alla fine")


def get_tags(browser):
    try:
        tags_elements = WebDriverWait(browser, 2).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='tags_container']/div[*]/a")))
        # tags_elements = browser.find_elements_by_xpath("//*[@id='tags_container']/div[*]/a")
        tags_lists = []
        for i in range(tags_elements.__len__()):
            tags_lists.append(tags_elements[i].text)
        print(tags_lists)
    except:
        print("no tags")

