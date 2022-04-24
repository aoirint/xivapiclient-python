import requests
from pydantic import BaseModel
import pickle


def load_cookies():
  with open('cookies.pkl', 'rb') as fp:
    _cookies = pickle.load(fp)
  cookies = {}
  for cookie in _cookies:
    domain = cookie['domain']
    if domain in ['.pixiv.net', '.www.pixiv.net']:
      cookies[cookie['name']] = cookie['value']
  return cookies


word = input('Keyword: ')

url = f'https://www.pixiv.net/ajax/search/artworks/{word}'

class Params(BaseModel):
  word: str
  order: str
  mode: str
  p: int
  s_mode: str
  type: str
  lang: str

params = Params(
  word=word,
  order='date_d',
  mode='all',
  p=1,
  s_mode='s_tag_full',
  type='all',
  lang='ja',
).dict()

cookies = load_cookies()

s = requests.Session()
s.cookies.update(cookies)
s.headers.update({
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
})

res = s.get(url, params=params)

with open('result.json', 'w', encoding='utf-8') as fp:
  fp.write(res.text)
