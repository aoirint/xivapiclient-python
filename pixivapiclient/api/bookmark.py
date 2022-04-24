import traceback
import pickle
from datetime import datetime
from pydantic import BaseModel, ValidationError
from typing import List

from ..util import create_session
from .model import IllustMangaData

# Request
class BookmarkParams(BaseModel):
  tag: str
  offset: int
  limit: int
  rest: str
  lang: str

# Response
class BookmarkResponseData(BaseModel):
  works: List[IllustMangaData]
  total: int

class BookmarkResponse(BaseModel):
  error: bool
  message: str
  body: BookmarkResponseData

def fetch_user_id() -> str:
  url ='https://www.pixiv.net'

  session = create_session()
  res = session.get(url)

  user_id = res.headers['x-userid']
  return user_id

def get_bookmarks(
  page: int = 1,
) -> BookmarkResponse:
  user_id: str = fetch_user_id()
  url = f'https://www.pixiv.net/ajax/user/{user_id}/illusts/bookmarks'

  params = BookmarkParams(
    tag='',
    offset=(page-1)*48,
    limit=48,
    rest='show',
    lang='ja',
  ).dict()

  session = create_session()
  res = session.get(url, params=params)

  try:
    response = BookmarkResponse.parse_obj(res.json())
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

  return response
