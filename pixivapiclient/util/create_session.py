import pickle
import requests
from typing import Dict

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'

def load_cookies() -> Dict[str, str]:
  with open('cookies.pkl', 'rb') as fp:
    _cookies = pickle.load(fp)

  cookies = {}
  for cookie in _cookies:
    domain = cookie['domain']
    if domain in ['.pixiv.net', '.www.pixiv.net']:
      cookies[cookie['name']] = cookie['value']

  return cookies


def create_session() -> requests.Session:
  cookies = load_cookies()

  session = requests.Session()
  session.cookies.update(cookies)
  session.headers.update({
    'User-Agent': useragent,
  })

  return session
