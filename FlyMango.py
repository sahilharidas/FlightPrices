# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:22:16 2020

@author: SahilHP
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import py_mail as mail

from datetime import date, datetime, timedelta
from os import remove
from os.path import exists
import pandas as pd


def selectDay(day):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'td.available'))
                                        )
    days = driver.find_elements_by_css_selector('td.available')
    while (days[0].text != '1'):
        days.remove(days[0])
        pass
    for d in days:
        if(int(d.text) == day):
            d.click()
            break
            pass
        pass
    pass

def fillForm(depart, arrive, day, month, setAirports):
    if (setAirports):
        driver.find_element_by_id('fromAirportWrapper').click()
        driver.find_element_by_partial_link_text(depart).click()
        driver.find_element_by_id('toAirportWrapper').click()
        driver.find_element_by_partial_link_text(arrive).click()
        pass
    
    #driver.find_element_by_css_selector('#flightDateRangePicker div').click()
    datePicker = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#flightDateRangePicker div'))
                                        )
    datePicker.click();
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
    
    driver.find_element_by_id('continueLink').click()
    pass

def extractInfo():
    dTime = driver.find_elements_by_css_selector('div.segment-summary__time')
    #aTime = driver.find_elements_by_css_selector('div.segment-summary__time.right')
    price = driver.find_elements_by_xpath(
            "//div[@class='fare-type__price-container']/span")
    #duration = driver.find_elements_by_css_selector('div.segment-summary__duration')
    #flightNo = driver.find_elements_by_css_selector('div.segment-summary__flight-number.right')
    #print(dTime, aTime, price, duration, flightNo, '\n')
    return dTime, price

def extractTimes():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.segment-summary__time"))
        )
    return driver.find_elements_by_css_selector('div.segment-summary__time')
    
def extractPrices():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
        "//div[@class='fare-type__price-container']/span"))
        )
    return driver.find_elements_by_xpath(
            "//div[@class='fare-type__price-container']/span")
    
def extractDurations():
    return driver.find_elements_by_css_selector('div.segment-summary__duration')

def toString(depart, arrive, dTime, price, date):
    #print(len(dTime), len(aTime), len(price), len(duration), len(flightNo))
    strOut = ''
    strOut += 'Mango Airlines\n'
    strOut += '{} - {}\n{}\n'.format(depart, arrive, date.strftime('%d %b %Y'))
    l = len(dTime)
    if (l > 0):
        for i in range(len(dTime)//2):
            strOut += '{} - {}: {}\n'.format(dTime[2*i].text,
                       dTime[2*i + 1].text, price[5*i + 1].text)
            pass
        pass
    return strOut

def toCSV(depart, arrive, date, times, prices, airline):
    strOut = ''
    l = len(times) // 2
    for i in range(l):
        strOut += '{},{},{},{},{},{},{},{}\n'.format(airline, depart, arrive,
                   date, date.today(), times[2*i].text,
                   times[2*i+1].text, prices[5*i + 1].text)
        #strOut += ','.join([airline, start, end, date, times[2*i].text,
         #          durations[i].text, prices[5*i + 1].text])
        pass
    return strOut
        

def saveData(data, filename):
    #print(data)
    file = open(filename, 'a')
    file.write(data)
    file.close()
    pass

'''def yeet(depart, arrive):
    if exists(file_prices):
        remove(file_prices)
        pass
    for i in pd.date_range(startDate, endDate):
        driver.get('https://www.flymango.com/')
        day = i.day
        month = i.strftime('%b')
        if (i.date() == startDate):
            changeDestination = True
        else:
            changeDestination = False
            pass
        fillForm(depart, arrive day, month, changeDestination)
        times, prices = extractTimes(), extractPrices()
        message = toString(depart, arrive, times, prices, i)
        saveData(message, file_prices)
        #saveData()
        pass
    driver.close()
    #mail.main('contacts.txt', 'FlightPrices.txt')
    pass'''

def changeSearch():
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-summary__change')))
    button.click()

def genData(depart, arrive, s, n):
    global driver
    driver = webdriver.Chrome(executable_path = path, options=chrome_options)
    startDate, endDate = date.today() + timedelta(days=s), date.today() + timedelta(days=s+n)
    driver.get('https://www.flymango.com/')
    for i in pd.date_range(startDate, endDate):
        currDate = i.date()
        day = i.day
        month = i.strftime('%b')
        if (currDate == startDate):
            changeDestination = True
        else:
            changeDestination = False
            pass
        fillForm(depart, arrive, day, month, changeDestination)
        times, prices = extractTimes(), extractPrices()
        data = toCSV(depart, arrive, currDate, times, prices, 'Mango')
        saveData(data, file_data)
        changeSearch()
        pass
    driver.close()
    pass

start = 'DUR'
end = 'CPT'
startDate = date(2020, 2, 2)
endDate = date(2020, 2, 2)

file_prices = 'FlightPrices.txt'
file_data = 'FLIGHT\\flight_data_{}.txt'.format(date.today())

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

path = r'C:\\Users\\SahilHP\\Downloads\\chromedriver_win32\\chromedriver'
driver = webdriver.Chrome(executable_path = path, options=chrome_options)

#yeet();
print(datetime.now())
#genData('DUR', 'CPT', 3, 120)
genData('CPT', 'DUR', 3, 120)
print(datetime.now())

'''driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 600) 

target = 'Mummy'
  
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located(( 
    By.XPATH, x_arg))) 
group_title.click() 
inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located(( 
    By.XPATH, inp_xpath))) 
for i in range(100): 
    input_box.send_keys(strOut + Keys.ENTER) 
    time.sleep(1) '''
