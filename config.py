import os
import math
CUR_DIR = os.path.abspath(os.getcwd())
DOWNLOAD_PATH = f"{CUR_DIR}\DOWNLOAD_DIRECTORY"

HEADLESS = False
TIME_OUT = 30
UPLOAD_TIME_OUT = 150
TIME_SLEEP = 5
MAX_SIZE_UPLOADS = 490*math.pow(1024,2)
SPLIT_SIZE = 100*math.pow(1024,2)

ICANN_URL = "https://account.icann.org/login"
ICANN = {
    "email": "email",
    "password": "password"
}

CZDS_TITLE = "Centralized Zone Data Service (CZDS)"

SPLUNK = {
    "host": "127.0.0.1",
    "port": 8000,
    "username": "administrator", 
    "password": "administrator" 
}

SPLUNK_URL = f"http://{SPLUNK['host']}:{SPLUNK['port']}/en-US/account/login"
SPLUNK_HOME_URL = f"http://{SPLUNK['host']}:{SPLUNK['port']}/en-US/app/launcher/home"
ADD_DATA_URL = f"http://{SPLUNK['host']}:{SPLUNK['port']}/en-US/manager/search/adddata"
LOGGER_NAME = "ICANN_SPLUNK_LOGGER"
LOG_FILE = "Log.log"
PLUNK_AGENT = "SPLUNK"
ICANN_AGENT = "ICANN"
DIR_AGENT = "DOWNLOAD_DIRECTORY"
