from selenium import webdriver
from selenium.webdriver.common.by import By
from METAR_TO_DB import MySQLConnection_RawData
from MetarCategory import MetarCategoryFunction
import time

#Scrapes the web for the data
driver = webdriver.Chrome()
driver.get('https://ilmailusaa.fi/weather-flightpath.html?location#select-area=1#textproduct-querysettings-radius=100#observation-mode=metar#obsManualLookup0=EFUT#id=radar/js')
time.sleep(1)
element = driver.find_element(By.XPATH, '//*[@id="observations"]/li/div[2]/p[1]')

#Formats the data so the MySQLConnection functions works as intended
METAR = element.text
METARinlist = (METAR,)

#Calls the function wich uploads the data to the MySQL database
MySQLConnection_RawData(METARinlist)

#Calls the fucntion wich categorises the data and uploads it to the MySQL database
MetarCategoryFunction(METARinlist)

#Closes the website connection
driver.quit()