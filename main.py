from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver


# auto_chromedriver = chromedriver_autoinstaller.install() TODO Certificate issue
auto_chromedriver = "/Users/andreacannizzo/WorkSpace/N26/venv/lib/python3.9/" \
                    "site-packages/chromedriver_autoinstaller/94/chromedriver"
browser = webdriver.Chrome(auto_chromedriver)
browser.get('https://app.n26.com/login')
login(browser, username, password)

# Commentato perchè in prova è troppo lungo
# scroll_to_bottom(browser)

# "//li/" for web elements, "//li/div/p/span/span[1]/a" to obtain href of each element
# but the element whit the href is not clickable
URL_elements = browser.find_elements_by_xpath("//li/div/p/span/span[1]/a")
URL_lists = []
for i in range(URL_elements.__len__()):
    # print(i)
    URL_lists.append(URL_elements[i].get_attribute("href"))
    # open new tab, go there and load page
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(URL_lists[i])
    # retrieve data
    get_tags(browser)
    # close new tab and go back to main
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

browser.close()
