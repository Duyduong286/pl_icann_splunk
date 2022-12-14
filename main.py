import os
import time
import gzip
import math
import config
import shutil
import schedule 
import icann_bot
import splunk_bot
from logger import create_logger
from filesplit.split import Split

def upload_files():
    splunk_bot.init_driver()
    if splunk_bot.login(config.SPLUNK["username"], config.SPLUNK["password"]):
        logger.info("Login success!", extra = {"agent" : config.SPLUNK_AGENT})
        try:
            splunk_bot.navigate()
            files = os.listdir(config.DOWNLOAD_PATH)
            if len(files) == 0:
                logger.warning(f"Nothing to upload! - PATH: {config.DOWNLOAD_PATH}", extra = {"agent" : config.DIR_AGENT})
            else:
                for file in files:
                    if file.endswith("txt"):
                        try:
                            path = os.path.join(config.DOWNLOAD_PATH, file)
                            splunk_bot.upload(path=path)
                            logger.info(f"File uploaded successfully! - PATH: {path} - SIZE: {size(path)}", extra = {"agent" : config.SPLUNK_AGENT})
                        except:
                            logger.error(f"Can't upload files: {path}", extra = {"agent" : config.SPLUNK_AGENT})
                        
                        splunk_bot.add_more_data()
                    else:
                        logger.info(f"Invalid file format to upload! - PATH: {path} - SIZE: {size(path)}", extra = {"agent" : config.SPLUNK_AGENT})
        except Exception as e:
            logger.error(f"{str(e)}", extra = {"agent" : config.SPLUNK_AGENT})
            logger.error(f"Can't upload files: {path}", extra = {"agent" : config.SPLUNK_AGENT})
    else:
        logger.error("Login failed or Connection Failure!", extra = {"agent" : config.SPLUNK_AGENT})
    splunk_bot.quit()

def download_files():
    icann_bot.init_driver()
    if icann_bot.login():
        logger.info("Login success!", extra = {"agent" : config.ICANN_AGENT})
        icann_bot.nav_czds()
    else:
        logger.error("Login failed or Connection Failure!", extra = {"agent" : config.ICANN_AGENT})
        icann_bot.quit()
        return False

    try:
        logger.info(".................DOWNLOADING!!!................", extra = {"agent" : config.ICANN_AGENT})
        num_files = icann_bot.get_czds_files()
    except:
        logger.info("Error while trying to download data!", extra = {"agent" : config.ICANN_AGENT})

    time.sleep(config.TIME_SLEEP)
    check = check_file_download(num_files)
    icann_bot.quit()
    return True and check

def check_file_download(num_files):
    while(True):
        files = os.listdir(config.DOWNLOAD_PATH)
        if len(files) == 0 :
            logger.warning(f"Can't download anything!", extra = {"agent" : config.ICANN_AGENT})
            return False

        for i in range(0, len(files)):
            if files[i].endswith('.crdownload'):
                time.sleep(config.TIME_SLEEP)
                files = os.listdir(config.DOWNLOAD_PATH)
                break

            if (len(files) < num_files) :
                time.sleep(config.TIME_SLEEP)
                if files != os.listdir(config.DOWNLOAD_PATH) : break

            if(i == len(files) - 1):
                logger.info(f"Download files successfully! - {len(files)}/{num_files} files", extra = {"agent" : config.ICANN_AGENT})
                return True

def clear_files():
    files = os.listdir(config.DOWNLOAD_PATH)
    if len(files) > 0:
        for file in files:
            path = os.path.join(config.DOWNLOAD_PATH, file)
            _size = size(path)
            try:
                os.remove(path)
                logger.info(f"Remove the file successfully! - PATH: {path} - SIZE: {_size}", extra = {"agent" : config.DIR_AGENT})
            except:
                logger.warning(f"Can't remove the file! - PATH: {path} - SIZE: {_size}", extra = {"agent" : config.DIR_AGENT})
    else:
        logger.warning(f"Nothing to remove! - PATH: {config.DOWNLOAD_PATH}", extra = {"agent" : config.DIR_AGENT})

def remove_file(path : str):
    try:
        _size = size(path)
        os.remove(path)
        logger.warning(f"Remove the file {path} - SIZE: {_size}", extra = {"agent" : config.DIR_AGENT})
    except Exception as e:
        logger.error(f"{str(e)}", extra = {"agent" : config.DIR_AGENT})

def size(path : str):
    size_bytes = os.path.getsize(path)
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def extract():
    files = os.listdir(config.DOWNLOAD_PATH)
    if len(files) == 0:
        logger.warning(f"Nothing to extract! - PATH: {config.DOWNLOAD_PATH}", extra = {"agent" : config.DIR_AGENT})
        return

    for file in files:
        path = os.path.join(config.DOWNLOAD_PATH, file)
        ex_file_name = '.'.join((file.split('.')[0],"txt"))
        new_path = os.path.join(config.DOWNLOAD_PATH, ex_file_name)
        try:
            with gzip.open(path, 'rb') as f_in:
                with open(new_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    logger.info(f"Extract the file successfully!: {new_path} - SIZE: {size(new_path)}", extra = {"agent" : config.DIR_AGENT})
            remove_file(path)
        except Exception as e:
            logger.error(f"{str(e)}", extra = {"agent" : config.DIR_AGENT})
            logger.error(f"Can't extract files: {path} - SIZE: {size(path)}", extra = {"agent" : config.DIR_AGENT})
            remove_file(path)
            remove_file(new_path)

def end():
    try:
        icann_bot.quit()
        splunk_bot.quit()
    except:
        pass
    finally:
        logger.info(".................DONE!!!................", extra = {"agent" : config.AGENT})
        
def split_file():
    files = os.listdir(config.DOWNLOAD_PATH)
    if len(files) == 0:
        logger.warning(f"Nothing to split! - PATH: {config.DOWNLOAD_PATH}", extra = {"agent" : config.DIR_AGENT})
        return
    
    for file in files:
        path = os.path.join(config.DOWNLOAD_PATH, file)
        if os.path.getsize(path) > config.MAX_SIZE_UPLOADS:
            split = Split(path, config.DOWNLOAD_PATH) 
            split.bysize(size=config.SPLIT_SIZE, newline=True)
            remove_file(path)
            remove_file(os.path.join(config.DOWNLOAD_PATH, "manifest"))
    pass

def del_data():
    splunk_bot.init_driver()
    if splunk_bot.login(config.DEL_USR["username"], config.DEL_USR["password"]):
        logger.info("Login success!", extra = {"agent" : config.SPLUNK_AGENT})
        try:
            logger.info(".................DELETING!!!................", extra = {"agent" : config.SPLUNK_AGENT})
            info_events = splunk_bot.del_all_data()
            logger.info(f"Deleted: {info_events}", extra = {"agent" : config.SPLUNK_AGENT})
            splunk_bot.quit()
            return True
        except Exception as e:
            logger.error(f"{str(e)}", extra = {"agent" : config.SPLUNK_AGENT})
            logger.error(f"Error while trying to delete data!", extra = {"agent" : config.SPLUNK_AGENT})
            splunk_bot.quit()
    else:
        logger.error("Login failed or Connection Failure!", extra = {"agent" : config.SPLUNK_AGENT})
    return False

def job():
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.mkdir(config.DOWNLOAD_PATH)

    clear_files()
    if download_files() :
        if del_data():
            extract()
            split_file()
            upload_files()
    end()

if __name__ == "__main__":
    global logger 
    logger = create_logger(config.LOGGER_NAME, config.LOG_FILE)
    job()
    schedule.every().tuesday.at("08:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
