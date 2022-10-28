import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

def init_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.headless = config.HEADLESS
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options)
    driver.set_page_load_timeout(config.TIME_OUT)

def login():
    try:
        driver.get(config.SPLUNK_URL)
        WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(config.SPLUNK["username"])
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(config.SPLUNK["password"])
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/form/fieldset/input[1]').click()
        WebDriverWait(driver, config.TIME_OUT).until(EC.url_contains("home"))
    except:
        return False
    return True

def navigate():
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/header/div[1]/div/a')))
    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/a').click()
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="AddData"]')))
    driver.find_element(By.XPATH, '//*[@id="AddData"]').click()
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[4]/div/div[1]/a/div/div[1]')))
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div/div[1]/a/div/div[1]').click()

def upload(path):
    #load file
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div/div[1]/div[2]/a')))
    select_button = driver.find_element(By.XPATH, '//*[@id="inputReference"]')
    select_button.send_keys(path)

    #next
    WebDriverWait(driver, config.UPLOAD_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '//div[@class="progress-bar"][@style="width: 100%;"]')))
    WebDriverWait(driver, config.UPLOAD_TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="nav-buttons"]/a[2]')))
    driver.find_element(By.XPATH, '//div[@class="nav-buttons"]/a[2]').click()

    #drop menu
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH,'//div[@class="source-info"]/div[@style="float:left;"]')))
    driver.find_element(By.XPATH, '//div[@class="source-info"]/div[@style="float:left;"]').click()
    WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="search-query text-clear "]' )))
    driver.find_element(By.XPATH, '//input[@class="search-query text-clear "]').send_keys("icann_txt")
    WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//ul[@class="dropdown-menu-main"]/li/a[@data-item-value="icann_txt"]')))
    driver.find_element(By.XPATH, '//ul[@class="dropdown-menu-main"]/li/a[@data-item-value="icann_txt"]').click()

    driver.find_element(By.XPATH, '//div[@class="nav-buttons"]/a[2]').click()
    driver.find_element(By.XPATH, '//div[@class="nav-buttons"]/a[2]').click()  
    driver.find_element(By.XPATH, '//div[@class="nav-buttons"]/a[2]').click() #submit

    WebDriverWait(driver, config.UPLOAD_TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '//div[@class="success-header"]')))

def add_more_data():
    driver.get(config.ADD_DATA_URL)
    WebDriverWait(driver, config.TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '//div[@class="type-container------dev---2cb8R"]/a')))
    driver.find_element(By.XPATH, '//div[@class="type-container------dev---2cb8R"]/a').click()

# def create_src_type():
#     driver.get(config.SPLUNK_HOME_URL)
#     WebDriverWait(driver, config.TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="type-container------dev---2cb8R"]/a')))
#     pass

def close():
    driver.close()

def quit():
    driver.quit()

