#!/usr/bin/python


# core
import collections
import logging
import pprint
import time

# 3rd party
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
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
driver.set_window_size(1200,1100)

driver.get(base_url)

driver.find_element_by_class_name('dropdown-toggle').click()
driver.find_element_by_name('username').send_keys(login.username)
driver.find_element_by_name('password').send_keys(login.password)
driver.find_element_by_xpath('//form/button').click()

def bitcoins_top():
    return float(driver.find_element_by_class_name('balanceraw-BTC').text)

def bitcoins_bottom():
    return float(driver.find_element_by_class_name('symbol2-available').text)

def element_html(elem):
    return elem.get_attribute('outerHTML')

SellOrder = collections.namedtuple('SellOrder', ['ask', 'amount'])

def loop_forever():
    while True: pass

def scroll_down():
    #driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));");
    driver.execute_script("window.scrollBy(250, 750)");

def sell_orders():
    scroll_down()
    #xpath = '//tr[contains(@class,"sell_tr")]'
    xpath = '//table[@id="md-sell"]/tbody/tr'
    print 1
    trs = WebDriverWait(driver, 90).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    trs = iter(trs)
    while True:
        try:
            tr = trs.next()
            _tds = tr.find_elements_by_tag_name('td')
            tds = []
            print "tds = {0}".format(pp.pformat(_tds))
            for td in _tds:
                tds.append(float(td.text))
            so = SellOrder(*tds[0:2])
            yield so
        except StaleElementReferenceException:
            continue
        except StopIteration:
            pass

def place_order(amount, price):
    driver.find_element_by_id('buy-amount').send_keys(str(amount))
    driver.find_element_by_id('buy-price').send_keys(str(price))
    driver.find_element_by_xpath(
        '//form[@id="buy"]/fieldset/div/button').click()
    button = WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.ID, 'confirm-ok')))
    button.click()

def order_hashes(so):
    b = bitcoins_bottom()
    amount = min( b / so.ask , so.amount)
    place_order( amount, so.ask )

def main():
    for so in sell_orders():
        order_hashes(so)
        break

if __name__ == '__main__':
    main()
