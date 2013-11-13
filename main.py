# core
import collections
import logging
import pprint
import time

# 3rd party
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# local
import cex
import login

pp = pprint.PrettyPrinter(indent=4)


base_url = 'https://cex.io'

driver = webdriver.Firefox()
driver.get(base_url)

driver.find_element_by_class_name('dropdown-toggle').click()
driver.find_element_by_name('username').send_keys(login.username)
driver.find_element_by_name('password').send_keys(login.password)
driver.find_element_by_xpath('//form/button').click()

def bitcoins():
    # return float(driver.find_element_by_class_name('balanceraw-BTC').text)
    return float(driver.find_element_by_id('symbol2-available').text)

print 'btc =', bitcoins()

def element_html(elem):
    return elem.get_attribute('outerHTML')

SellOrder = collections.namedtuple('SellOrder', ['ask', 'amount'])

def loop_forever():
    while True: pass


def sell_orders():
    #xpath = '//tr[contains(@class,"sell_tr")]'
    xpath = '//table[@id="md-sell"]/tbody/tr'
    print 1
    trs = WebDriverWait(driver, 90).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    for i, tr in enumerate(trs):
        print i
        #print element_html(tr)
        tds = [float(td.text) for td in tr.find_elements_by_tag_name('td')]
        so = SellOrder(*tds[0:2])
        yield so

def place_order(amount, price):
    driver.find_element_by_id('buy-amount').send_keys(str(amount))
    driver.find_element_by_id('buy-price').send_keys(str(price))
    driver.find_element_by_xpath(
        '//form[@id="buy"]/fieldset/div/button').click()
    button = WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.ID, 'confirm-ok')))
    button.click()


def order_hashes(so):
    b = bitcoins()
    amount = min( b / so.ask , so.amount)
    place_order( amount, so.ask )

def main():
    for so in sell_orders():
        order_hashes(so)
        time.sleep(10)
        print 'Bitcoins remaining', bitcoins()

if __name__ == '__main__':
    main()
