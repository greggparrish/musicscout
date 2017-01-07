#!/usr/bin/python3

"""
  TODO:
  - download media if < 10 min
  - log
"""

import datetime
import os
import re
from time import mktime


from bs4 import BeautifulSoup
import feedparser
import requests
from slugify import slugify
import youtube_dl

from config import Config
import db
from utils import Utils

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
      line = line.replace('\n','').strip()
      line = line.split('|')
      try:
        genre = slugify(line[1])
      except:
        genre = 'uncategorized'
      if line[0]:
        feed = line[0].strip()
        d.add_url(feed)
        feeds += [[feed,genre]]
        self.get_media_links(feed, genre)
        timestamp = datetime.datetime.now()
        d.update_time(feed,timestamp)
    feedfile.close()
    return feeds

  def get_media_links(self, feed, genre):
    """ get posts for a feed, strip media links  """
    last_update = d.feed_time(feed)[0]
    lu = None
    posts = feedparser.parse(feed)
    media_sites = ['youtu', 'bandcamp', 'soundcloud', 'redditmedia']
    if last_update:
      lu = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S.%f')
    try:
      ft = datetime.datetime.fromtimestamp(mktime(posts.modified_parsed))
    except:
      ft = None
    if not lu or not ft or ft > lu:
      print("checking posts for {}".format(feed))
      for p in posts.entries:
        pt = datetime.datetime.fromtimestamp(mktime(p.updated_parsed))
        if not lu or pt > lu:
          try:
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
          except:
            pass

  def yt_dl(self, link, genre):
    genre_dir = os.path.join(c['cache_dir'],genre)
    ydl_opts = {
        'outtmpl' : genre_dir+'/%(title)s_%(id)s.%(ext)s',
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
feeds = ms.get_urls()
