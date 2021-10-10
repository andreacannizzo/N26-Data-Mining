from inputs import *
from definitions import *
import chromedriver_autoinstaller
from selenium import webdriver


auto_chromedriver = chromedriver_autoinstaller.install()
browser = webdriver.Chrome(auto_chromedriver)
browser.get('https://app.n26.com/login')
login(browser, username, password)
scroll_to_bottom(browser)
# "//li/" for web elements, "//li/div/p/span/span[1]/a" to obtain href of each element
# but the element whit the href is not clickable
URL_elements = browser.find_elements_by_xpath("//li/div/p/span/span[1]/a")

# elemento freccia in basso espandi pagina
# from selenium.webdriver.common.keys import Keys
# button = browser.find_element_by_xpath("//*[@title='Successivo' and @type='button']")
# button.send_keys(Keys.RETURN)

# per creare un elemento ogni transazione visibile nella pagina
# browser.find_elements_by_xpath("//li/div/p/span/span[1]/a")

browser.close()
