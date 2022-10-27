import time 
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

def init_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.headless = config.HEADLESS
    options.add_experimental_option("prefs", 
                                    {"download.default_directory" : config.DOWNLOAD_PATH, 
                                    "safebrowsing.enabled" : "false",
                                    'profile.default_content_setting_values.automatic_downloads': 1
                                    })
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options)
    driver.set_page_load_timeout(config.TIME_OUT)

def close():
    driver.close()

def login():
    try:
        driver.get(config.ICANN_URL)
        WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailAddressOrUsername"]')))
        login = driver.find_element(By.CLASS_NAME, "form-control")
        login.send_keys(config.ICANN["email"])
        WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitUsername"]')))
        time.sleep(5)
        driver.find_element(By.ID, 'submitUsername').click()
        WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="form-control"]' and '//input[@type="password"]')))
        passw = driver.find_element(By.XPATH, '//*[@class="form-control"]' and '//input[@type="password"]')
        passw.send_keys(config.ICANN["password"]) 
        passw.send_keys(Keys.RETURN)
        WebDriverWait(driver, config.TIME_OUT).until(EC.url_contains("userhome"))
    except:
        return False

    return True

def navigate(title : str):
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH, f'//*[@title="{title}"]')))
    path = driver.find_element(By.XPATH, f'//*[@title="{title}"]')
    path.click()


def get_czds_files():
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tld')))
    approved = driver.find_element(By.CSS_SELECTOR, 'a.button:nth-child(3)').get_attribute('href')
    driver.get(approved)
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.table-sortable > tbody:nth-child(2)'))) 
    time.sleep(2)
    downloads = driver.find_elements(By.CSS_SELECTOR, '.table-sortable > tbody:nth-child(2) > tr')

    for i in range(1, len(downloads) + 1):
        try:
            WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'.table-sortable > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(6) > a:nth-child(1)')))
            button = driver.find_element(By.CSS_SELECTOR, f'.table-sortable > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(6) > a:nth-child(1)')
            driver.execute_script("arguments[0].click();", button)
            # break
        except:
            pass
    
