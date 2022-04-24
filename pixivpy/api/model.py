
from pydantic import BaseModel
from typing import List, Optional, Union

# Response
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
