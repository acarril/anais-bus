import string
import random
import urllib
import time
import subprocess
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def initDriver(headless = False):
    '''Initialize web driver with paramenters'''

    # Driver parameters
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.headless = headless

    # Insatiate webdriver
    driver = webdriver.Chrome(options = chrome_options)
    driver.set_page_load_timeout(30)

    # Handle driver loading
    return(driver)

# def pwd_generator(size=8, chars=string.ascii_letters + string.digits + '!@#$%^&*()_'):
#     return ''.join(random.choice(chars) for _ in range(size))å

def gen_pwd(size=8):
    random_source = string.ascii_letters + string.digits + '@#!_'
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol
    password += random.choice('@#!_')

    # generate other characters
    for i in range(size-4):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

def gen_email():
    name = random.choice(open('names.csv').readlines()).rstrip()
    surname = random.choice(open('surnames.csv').readlines()).rstrip()
    randint = random.randrange(0,4)
    email = name.lower()[0:randint]
    if randint > 0:
        email += random.choice('._')
    email += surname.lower()
    if random.randrange(0,2) == 0:
        if random.randrange(0,2) == 0:
            email += random.choice('._')
        email += random.choice('789') + random.choice(string.digits)
    email += '@gmail.com'
    return email

def countFun(fun):
    '''Count number of times a function is called'''
    def wrapper(*args, **kwargs):
        wrapper.counter += 1    # executed every time the wrapped function is called
        return fun(*args, **kwargs)
    wrapper.counter = 0         # executed only once in decorator definition time
    return wrapper

@countFun # globally count number of times run to index vpn_codes
def switchVpn(country = 'USA'):
    '''Switch VPN connection, exhausting list of country codes'''
    # Fetch country codes
    def getVpnCountryCodes(country = None):
        process = subprocess.Popen('expressvpn list all'.split(), stdout = subprocess.PIPE)
        stdout = str(process.communicate()[0], 'utf-8')
        if country == None:
            countryCodes = re.findall(fr"^([^ \t]+).*", stdout, re.MULTILINE)
        else:
            countryCodes = re.findall(fr"^us[^\s]+", stdout, re.MULTILINE)
        return(countryCodes)
    
    vpn_codes = getVpnCountryCodes(country = 'USA')
    code = random.choice(vpn_codes)
    os.system('expressvpn disconnect')
    os.system(f'expressvpn connect {code}')
    print(f'VPN connected to code {code}')

# Init driver and VPN connection
switchVpn(country = 'USA')
driver = initDriver()

url = 'https://www.ourbus.com/invitation/OBBQDQJM/438102'
driver.get(url)

# Origin
origin_box = driver.find_element_by_id('source')
origin_box.send_keys('Philadelphia, PA 19104, USA')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(1)

# Destination
destination_box = driver.find_element_by_id('destination')
destination_box.send_keys('Princeton University, Princeton, NJ, USA')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(1)

# Arrival time
done_buttons = driver.find_elements_by_class_name('reset_time')
arrive_box = driver.find_element_by_id('timepicker_arrived')
arrive_box.send_keys('09:00 AM')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(1)
done_buttons[0].click()


# Destination time
done_buttons = driver.find_elements_by_class_name('reset_time')
destination_box = driver.find_element_by_id('timepicker_departure')
destination_box.send_keys('06:00 PM')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
time.sleep(1)
done_buttons[1].click()

# Remove timepicker from view
# driver.execute_script("document.getElementsByClassName('timepicker_wrap ')[1].style.display = 'none';")

# Join
join_button = driver.find_element_by_id('join')
join_button.click()


### PHASE TWO

# Email
email_box = driver.find_element_by_id('signuppage_email')
email = gen_email()
email_box.send_keys(email)
time.sleep(1)

# Password
pwd_box = driver.find_element_by_id('signuppage_password')
pwd_box.send_keys(gen_pwd())
time.sleep(1)

# Sign up
signup_button = driver.find_element_by_id('siguppage_btn_signup')
signup_button.click()
time.sleep(5)

# Confirm and close
try:
    confirm = driver.find_element_by_id('alert_message_cnf')
    print(confirm.text.split(' ', 1)[0] + ' ' + email)
except NoSuchElementException:
    print('fail :( ' + email)

os.system('expressvpn disconnect')
driver.close()





