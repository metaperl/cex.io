# core

# 3rd party
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# local
import login

base_url = 'https://cex.io'

driver = webdriver.Firefox()
driver.get(base_url)

driver.find_element_by_class_name('dropdown-toggle').click()
driver.find_element_by_name('username').send_keys(login.username)
driver.find_element_by_name('password').send_keys(login.password)

elem.click()
