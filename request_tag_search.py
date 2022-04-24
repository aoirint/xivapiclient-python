import traceback
import requests
from pydantic import BaseModel, ValidationError
import pickle
from typing import List, Optional, Union
from datetime import datetime

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

class TitleCaptionTranslation(BaseModel):
  workTitle: Optional[str]
  workCaption: Optional[str]

class BookmarkData(BaseModel):
  id: str
  private: bool

class IllustMangaData(BaseModel):
  id: str
  title: str
  illustType: int
  xRestrict: int
  restrict: int
  sl: int
  url: str
  description: str
  tags: List[str]
  userId: str
  userName: str
  width: int
  height: int
  pageCount: int
  isBookmarkable: bool
  bookmarkData: Optional[BookmarkData]
  alt: str
  titleCaptionTranslation: Optional[TitleCaptionTranslation]
  createDate: str
  updateDate: str
  isUnlisted: bool
  isMasked: bool
  profileImageUrl: str

class AdContainer(BaseModel):
  isAdContainer: bool

class IllustManga(BaseModel):
  data: List[Union[IllustMangaData, AdContainer]]

class ResponseData(BaseModel):
  illustManga: IllustManga
  relatedTags: List[str]

class Response(BaseModel):
  error: bool
  body: ResponseData

try:
  response = Response.parse_obj(res.json())
except ValidationError as error:
  ts = datetime.now().strftime('%Y%m%d_%H%M%S.%f')
  with open(f'error_{ts}.pkl', 'wb') as fp:
    pickle.dump({
      'response': res,
      'timestamp': ts,
      'error': error,
      'traceback': traceback.format_exc(),
    }, fp)
  raise error

data = response.body.illustManga.data

with open('result.json', 'w', encoding='utf-8') as fp:
  fp.write(response.json())
