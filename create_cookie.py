from selenium import webdriver
import pickle

driver = webdriver.Chrome()
driver.get('https://www.pixiv.net/')

input()

cookies = driver.get_cookies()
with open('cookies.pkl', 'wb') as fp:
  pickle.dump(cookies, fp)
