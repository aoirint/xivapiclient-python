from selenium import webdriver
import pickle

driver = webdriver.Chrome()
driver.get('https://www.pixiv.net/')

with open('cookies.pkl', 'rb') as fp:
  cookies = pickle.load(fp)

for cookie in cookies:
  domain = cookie['domain']
  if domain in ['.pixiv.net', '.www.pixiv.net']:
    driver.add_cookie(cookie)

driver.get('https://www.pixiv.net/')

input()
driver.quit()
