# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:59:23 2020

@author: SahilHP
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

start = 'DUR'
end = 'CPT'
date = date(2020, 6, 20)

path = r'C:\\Users\\SahilHP\\Downloads\\chromedriver_win32\\chromedriver'
driver = webdriver.Chrome(executable_path = path)
#driver.get('https://www.flysafair.co.za/')
site = '''https://www.flysafair.co.za/Flight/Search?interline=false
        &fromCityCode=CPT&toCityCode=DUR&departureDateString=2020-1-29
        &returnDateString=2020-1-29&adults=1&children=0&infants=0
        &roundTrip=false&useFlexDates=true&allInclusive=&promocode=
        &isSpecialAssistanceRequired=false&fareTypes=&currency=ZAR&showMonthView=false'''
driver.get('https://www.flysafair.co.za/')

driver.find_element_by_css_selector("input[type='radio'][value='one-way']").click()
Select(driver.find_element_by_id('departureCityDrop')).select_by_value(start)
Select(driver.find_element_by_id('arrivalCityDrop')).select_by_value(end)

driver.find_element_by_id('departureDate').click()
#driver.find_element_by_id('divpickercontainer-departureDate').click()
monthNotFound = True
    while (monthNotFound):
        firstMonth = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'th.month'))
                                        )
        firstMonth = firstMonth.text
        if (firstMonth.split()[0] == month):
            selectDay(day)
            monthNotFound = False
        else:
            driver.find_element_by_css_selector('th.next').click()
        pass

'''driver.find_element_by_name('searchButton').click()

#driver.implicitly_wait(45)
#driver.find_element_by_id('nav-icon3').click()

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.date-menu a.next-week'))
                                        ).click()
except:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.date-menu a.next-week'))
                                        ).click()
  

dTime = driver.find_element_by_css_selector('div.day-flight__dep div.day-flight__time').text
aTime = driver.find_element_by_css_selector('div.day-flight__arr div.day-flight__time').text
price = driver.find_element_by_css_selector('button.day-flight__price-lowest span'
                                            ).text.replace(',', '.')

print(dTime, aTime, price)

driver.close()'''