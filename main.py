from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import requests
from urllib.parse import urlparse
import os

delay = 30


def url_parse(url):
    u = urlparse(url)
    return os.path.join(f'{u.scheme}://', u.netloc)


def get_cookies(url=None, email=None, passwd=None):
    """Get cookies from Shopify shopping site"""
    if isinstance(url, str):
        url = os.path.join(url_parse(url), 'admin')

    browser = webdriver.Chrome()
    browser.get(url)
    try:
        time.sleep(5)
        WebDriverWait(browser, delay).until(ec.presence_of_element_located((By.CLASS_NAME, 'ui-button--primary')))
        email_field = browser.find_element_by_id('account_email')
        email_field.send_keys(email)
        next_btn = browser.find_element_by_class_name('ui-button--primary')
        next_btn.click()
        time.sleep(5)
    except TimeoutException:
        print("Loading took too much time!")

    try:
        WebDriverWait(browser, delay).until(ec.presence_of_element_located((By.CLASS_NAME, 'ui-button--primary')))
        account_password = browser.find_element_by_id('account_password')
        account_password.send_keys(passwd)

        next_btn = browser.find_element_by_class_name('ui-button--primary')
        next_btn.click()

        print("Login completed!")
    except TimeoutException:
        print("Loading took too much time!")
    cookies = browser.get_cookies()
    browser.quit()
    return cookies


def get_entity(url=None, api_version='2021-01', entity=None, id=None, since_id=None, limit=20, cookies=None):
    """Get entity from shopify via api depend cookies"""
    if isinstance(url, str):
        url = os.path.join(url_parse(url), 'admin')
    if id is not None:
        entity = f'{entity}.json?id={id}'
    elif since_id is not None:
        entity = f'{entity}.json?since_id={since_id}&limit={limit}'
    else:
        entity = f'{entity}.json'
    real_url = os.path.join(url, 'api', api_version, entity)

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get(real_url)
    if response.status_code == 200:
        return response.text
    else:
        print('General error.')
