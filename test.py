import time

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome('chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element(By.XPATH, '//input[@class="gLFyf gsfi"]')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()