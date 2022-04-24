from pixivapiclient.api.tag_search import AdContainer, search_tag

word = input('Keyword: ')

response = search_tag(word=word)
data = response.body.illustManga.data

for illustManga in data:
  if isinstance(illustManga, AdContainer):
    continue
  print(f'https://www.pixiv.net/artworks/{illustManga.id}: {illustManga.title}')
