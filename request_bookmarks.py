from pixivpy.api.bookmark import get_bookmarks

response = get_bookmarks()
works = response.body.works

print(f'Total: {response.body.total}')

for illustManga in works:
  print(f'https://www.pixiv.net/artworks/{illustManga.id}: {illustManga.title}')
