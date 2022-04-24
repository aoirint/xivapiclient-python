import traceback
import pickle
from datetime import datetime
from pydantic import BaseModel, ValidationError
from typing import List

from ..util import create_session
from .model import IllustManga

# Request
class TagSearchParams(BaseModel):
  word: str
  order: str
  mode: str
  p: int
  s_mode: str
  type: str
  lang: str

# Response
class TagSearchResponseData(BaseModel):
  illustManga: IllustManga
  relatedTags: List[str]

class TagSearchResponse(BaseModel):
  error: bool
  body: TagSearchResponseData


def search_tag(
  word: str,
  page: int = 1,
) -> TagSearchResponse:
  url = f'https://www.pixiv.net/ajax/search/artworks/{word}'

  params = TagSearchParams(
    word=word,
    order='date_d',
    mode='all',
    p=page,
    s_mode='s_tag_full',
    type='all',
    lang='ja',
  ).dict()

  session = create_session()
  res = session.get(url, params=params)

  try:
    response = TagSearchResponse.parse_obj(res.json())
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
