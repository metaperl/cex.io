# core
import collections
import logging

# 3rd party
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# local
import cex
import login

base_url = 'https://cex.io'

driver = webdriver.Firefox()
driver.get(base_url)

driver.find_element_by_class_name('dropdown-toggle').click()
driver.find_element_by_name('username').send_keys(login.username)
driver.find_element_by_name('password').send_keys(login.password)
driver.find_element_by_xpath('//form/button').click()

def bitcoins():
    return float(driver.find_element_by_class_name('balanceraw-BTC').text)

print 'btc =', bitcoins()


SellOrder = collections.namedtuple('SellOrder', ['ask', 'amount'])

def sell_orders():
    o = cex.CEX().order_book()
    return (SellOrder(tuple(o)) for o in o['asks'])

for s = sell_orders():
    amount_buyable = min(s.amount, bitcoins() / s.ask)
