import requests
from bs4 import BeautifulSoup


link = 'https://bandcamp.com/EmbeddedPlayer/album=25834495/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/transparent=true/'
player = BeautifulSoup(requests.get(link).content, 'lxml')
link = player.find('input', { "id" : "shareurl" } ).get('value') 
print(link)
