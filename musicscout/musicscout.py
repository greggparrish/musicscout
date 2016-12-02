#!/usr/bin/python3

"""
  TODO:
  - add/rm from db
  - for each url, get all media more recent than last_updated (or cutoff of a few months ago?)
  - download media if < 10 min
  - metadata?  Esp for yt clips
  - update mpd
  - add to mpd playlists: (scout_genre, and scout_genre_new [or scout_genre_date?]) config: naming pattern
  - exit after updating media from feeds
  - log
"""

import os
import re
import shutil
import sys
import time

from bs4 import BeautifulSoup
import configparser
import feedparser
import requests
from slugify import slugify
import youtube_dl

from config import Config
import db
from messages import Messages
from mpd import MPDQueue
from utils import Utils

c = Config().conf_vars()
d = db.Database()
ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

class Musicscout():
  def __init__(self):
    ut = Utils()
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
        feed = line[0]
        d.add_url(feed)
        feeds += [[feed,genre]]
        self.get_media_links(feed, genre)
    feedfile.close()
    return feeds

  def get_media_links(self, feed, genre):
    """ get posts for a feed, strip media links  """
    posts = feedparser.parse(feed)
    genre_dir = Config().build_dirs(os.path.join(c['cache_dir'], genre))
    for p in posts.entries:
      r = BeautifulSoup(requests.get(p.link).content, 'lxml')
      frames = r.find_all('iframe')
      for f in frames:
        link = f['src']
      if 'youtu' in link:
        self.yt_dl(p.link,genre)
      else:
        pass

  def yt_dl(self, link, genre):
    genre_dir = os.path.join(c['cache_dir'],genre) 
    ydl_opts = {
        'outtmpl' : genre_dir+'/%(title)s_%(id)s.%(ext)s',
        'format': 'bestaudio/best',
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
