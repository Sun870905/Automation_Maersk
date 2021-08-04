from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import json
import time

def acp_api_send_request(driver, message_type, data={}):
    message = {
        'receiver': 'antiCaptchaPlugin',
        'type': message_type,
        **data
    }
    return driver.execute_script("""return window.postMessage({});""".format(json.dumps(message)))

chrome_options = Options()

chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('blink-settings=imagesEnabled=false')  # disable images
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-javascript')
chrome_options.add_argument('--disable-plugins')
chrome_options.add_argument("--start-maximized")
anticaptcha_extension = "anticaptcha-plugin_v0.55.crx"
chrome_options.add_extension(anticaptcha_extension)

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

userID = 'aaron.baker'
password = 'Yld&1602'

try:
    driver.get("https://antcpt.com/blank.html")
    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {
            'enable': True,
            'antiCaptchaApiKey': 'f19dbd291990d441a2f3dc800bf5762e',
            'autoSubmitForm': False,
        }}
    )
    driver.get('https://www.maersk.com/portaluser/login')
    
    while 1:
        user = driver.find_element_by_id("usernameInput")
        user.clear()
        user.send_keys(userID)
        
        pwd = driver.find_element_by_id("passwordInput")
        pwd.clear()
        pwd.send_keys(password)
    
        element = driver.find_element_by_class_name("button--primary")
        element.click() # Login
        acp_api_send_request(
            driver,
            'setOptions',
            {'options': {
                'autoSubmitForm': True,
            }}
        )
        time.sleep(10)
        
        if driver.current_url == "https://www.maersk.com/portaluser/register/why-upgrade":
            break
        
        # else:
            # driver.refresh()
    
except TimeoutException:
    print('TimeoutException...60001')