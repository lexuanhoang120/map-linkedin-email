from selenium.common.exceptions import NoSuchElementException

import requests
import json
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
from tqdm import tqdm
import random
import uuid
from threading import Lock

import logging
import datetime
from traceback import print_exc

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

import os
os.environ['https_proxy'] = "http://proxy.hcm.fpt.vn:80/"
os.environ['http_proxy'] = "http://proxy.hcm.fpt.vn:80/"
os.environ['no_proxy'] = "localhost,127.0.0.0,127.0.1.1,127.0.1.1,local.home"


# Define your proxy
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = "http://hndc11.proxyxoay.net:62142"
proxy.ssl_proxy = "http://hndc11.proxyxoay.net:62142"


def write_to_file(data, filename='access_token.json'):
    file_lock = Lock()
    with file_lock:
        with open(filename, 'a') as f:
            f.write(json.dumps(data) + '\n')
            
def pass_privacy_notice(driver):
    if "privacynotice" in driver.current_url:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()
    return 0
    
def get_account_passwork():
    with open('resource/account.txt', 'r') as f:
        accounts = f.readlines()
    accounts = [account.replace('\n',"").split('|') for account in accounts]
    return accounts

def random_sleep(min_time, max_time):
    time.sleep(np.random.uniform(min_time, max_time))
    return 0

def get_author(token):
    session = requests.Session()
    paramsGet = {
        "AadObjectId": "",
        "Smtp": 'lionelmessi@gmail.com',
        "OlsPersonaId": "",
        "UserPrincipalName": "",
        "RootCorrelationId": str(uuid.uuid4()),
        "CorrelationId": str(uuid.uuid4()),
        "ClientCorrelationId": str(uuid.uuid4()),
        "PersonaDisplayName": "",
        "UserLocale": "en-US",
        "ExternalPageInstance": "00000000-0000-0000-0000-000000000000",
        "PersonaType": "User"
    }
    headers = {
        "Authorization": token,
        "X-ClientFeature": "LivePersonaCard",
        "Accept": "text/plain, application/json, text/json",
        "X-ClientType": "OwaMail",
        "X-HostAppCapabilities": "{}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Connection": "close",
        "X-LPCVersion": "1.20210418.1.0"
    }

    response = session.get(
        "https://sfnam.loki.delve.office.com/api/v1/linkedin/profiles/full", 
        params=paramsGet, 
        headers=headers
    )
    return response.status_code,response.text


def create_driver(headless=True):
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--window-size=1920,1200")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--proxy-server=http://proxy.hcm.fpt.vn:80')
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # # Set up logging preferences
    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'performance': 'ALL'}  # Enable performance logging
    
    # Create a Service object for ChromeDriver
    s = Service(executable_path='resource/chromedriver')
    
    # Initialize the WebDriver with the service, options, and capabilities
    driver = webdriver.Chrome(service=s, options=chrome_options)
    
    logging.info("Create driver successfully")
    
    driver.implicitly_wait(10)
    return driver



def get_access_token_from_outlook(account, first_name='Lionel', last_name = 'Messi', recipient_email = 'lionelmessi1997@gmail.com'):
    driver_wait_time = 10
    username = account[0]
    password = account[1]
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    proxy = "hndc11.proxyxoay.net:62142"
    # options.add_argument(f'--proxy-server=http://{proxy}')
    # add proxy to driver
    driver = create_driver()
    driver.get('https://outlook.office365.com/')
    random_sleep(2,4)
    try:



        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@id="meControl"]')))
        # driver.find_element(By.XPATH, '//div[@id="meControl"]').click()

        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Enter your email, phone, or Skype."]')))
        # email_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Enter your email, phone, or Skype."]')
        # email_input.send_keys(username)
        # driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        #
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'input[aria-label="Enter the password for {username}"]')))
        # password_input = driver.find_element(By.CSS_SELECTOR, f'input[aria-label="Enter the password for {username}"]')
        # password_input.send_keys(password)
        # driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        #
        # pass_privacy_notice(driver)
        #
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        # driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
        email_input.send_keys(username, Keys.ENTER)
        random_sleep(2,4)

        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_input.send_keys(password, Keys.ENTER)
        random_sleep(2,4)

        pass_privacy_notice(driver)

        try:
            if 'lock' in driver.find_element(By.CSS_SELECTOR, 'div[role="heading"]').text:

                write_to_file({'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               'account':username,'status_code':800,
                               'response':None,
                               'authorization':None}
                              )
                driver.quit()
                return (200,'Success')
        except:
            pass

        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Go to Outlook"]')))
        random_sleep(1,2)
        driver.get('https://outlook.live.com/people/')
        random_sleep(2,4)

        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="New contact"]')))

        try:
            WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@aria-label, "{first_name} {last_name}")]')))
            contact_tab = driver.find_element(By.XPATH, f'//div[contains(@aria-label, "{first_name} {last_name}")]')
            contact_tab.click()
        except:
            driver.find_element(By.CSS_SELECTOR, 'button[aria-label="New contact"]').click()

            WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="First name"]')))
            first_name_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="First name"]')
            first_name_input.send_keys(first_name)
            last_name_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Last name"]')
            last_name_input.send_keys(last_name)
            email_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Email address 1"]')
            email_input.send_keys(recipient_email)
            driver.find_element(By.CSS_SELECTOR, 'button[data-automation="LPESave"]').click()

            WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.XPATH, f'//div[contains(@aria-label, "{first_name} {last_name}")]')))
            driver.find_element(By.XPATH, f'//div[contains(@aria-label, "{first_name} {last_name}")]').click()

        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-content="Overview"]')))
        driver.find_element(By.CSS_SELECTOR, 'button[data-content="Overview"]').click()
        WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-log-name="PanelFooter"]')))
        network_data = driver.get_log('performance')
        driver.quit()

        network_data = [data for data in network_data if ('loki.delve.office.com/api/' in data['message'])&('Bearer' in data['message'])]
        token_list = ["Bearer " + data['message'].split('Bearer ')[1].split('"')[0].replace('\\','') for data in network_data]
        token_list = list(set(token_list))
        for token in token_list:
            write_to_file({'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'account':username,'status_code':get_author(token)[0],
                'response':get_author(token)[1],
                'authorization':token}
                )

        # write_to_file({'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #             'account':username,
        #             'authorization':token_list}
        #             )
        return (200,'Success')
    except Exception as e:
        driver.quit()
        print(f"Failed to get access token for account {account} {print_exc()}")
        return (400, str(e))

def get_token_from_outlook_main(account, first_name='Lionel', last_name = 'Messi', recipient_email = 'lionell_mes@gmail.com'):
    i = 0
    while i < 2:
        try:
            if get_access_token_from_outlook(account, first_name, last_name, recipient_email)[0] == 400:
                # print(f"Failed to get access token for account {account} ")
                i += 1
            else:
                # print(f"Success to get access token for account {account}")
                break
        except Exception as e:
            # print(f"Failed to get access token for account {account} {print_exc()}")
            i += 1
# get_access_token_from_outlook(('cafagnoagq674287@hotmail.com','cocW858bPN832'))

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_token_from_outlook_main, account) for account in get_account_passwork()]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing account"):
            try:
                future.result()
            except Exception as exc:
                print(f'Task generated an exception: {exc}')

main()