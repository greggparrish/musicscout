#!/usr/bin/python3

"""
  TODO:
  - download media if < 10 min
  - log
"""

import datetime
import os
import re
from time import mktime,sleep


from bs4 import BeautifulSoup
import feedparser
import requests
import youtube_dl

from config import Config
import db
from utils import Utils
from mpdutil import mpd_update, make_playlists

c = Config().conf_vars()
d = db.Database()
ut = Utils()
ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

class Musicscout():
  def __init__(self):
    ut.symlink_musicdir()
    #ut.clear_cache()

  def get_urls(self):
    """
    Open urls file in .config, make list
    """
    feeds = []
    feedfile = open(ConfigPath+'urls')
    for line in feedfile:
      line=line.strip()    
      if not line.startswith("#"):
        line = line.replace('\n','').strip()
        line = line.split('|')
        try:
          genre = re.sub(r'[-\s]+', '-', (re.sub(r'[^\w\s-]', '',line[1]).strip().lower()))
        except:
          genre = 'uncategorized'
        if line[0]:
          feed = line[0].strip()
          d.add_url(feed)
          feeds += [[feed,genre]]
          ft = self.get_media_links(feed, genre)
          d.update_time(feed,ft)
    feedfile.close()
    return feeds

  def get_media_links(self, feed, genre):
    print("checking posts for {}".format(feed))
    """ get posts for a feed, strip media links  """
    last_update = d.feed_time(feed)[0]
    lu = None
    posts = feedparser.parse(feed)
    media_sites = ['youtu', 'bandcamp', 'soundcloud', 'redditmedia']
    if last_update:
      lu = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
    try:
      ft = datetime.datetime.fromtimestamp(mktime(posts.feed.updated_parsed))
    except:
      ft = None
    if not lu or not ft or ft > lu:
      for p in posts.entries:
        pt = datetime.datetime.fromtimestamp(mktime(p.updated_parsed))
        if not lu or pt > lu:
          if ft == None or pt > ft:
            ft = pt
          try:
            sleep(3)
            r = BeautifulSoup(requests.get(p.link).content, 'lxml')
            frames = r.find_all('iframe')
            for f in frames:
              try:
                if 'bandcamp' in f['src']:
                  fl = re.search(r'href=[\'"]?([^\'" >]+)', str(f))
                  f_link = fl.group(1)
                  link = f_link
                else:
                  link = f['src']
                  f_link = ut.format_link(link)
                check_song = d.check_song(f_link)
                if not check_song and any(m in f_link for m in media_sites):
                  self.yt_dl(link,genre)
                  add_song = d.add_song(f_link)
              except: #Non-working link
                pass
          except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
    return ft

  def yt_dl(self, link, genre):
    genre_dir = os.path.join(c['cache_dir'],genre)
    ydl_opts = {
        'outtmpl' : genre_dir+'/%(title)s__%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'max-downloads': '3',
        'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
          }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      try:
        ydl.download([link])
      except:
        pass

ms = Musicscout()
ms.get_urls()
ut.clean_cache()
mpd_update()
sleep(10)
make_playlists()
