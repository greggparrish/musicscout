#!/usr/bin/python3


"""
  TODO:
  - read urls
  - add/rm from db
  - get all urls
  - for each url, get all media more recent than last_updated (or cutoff of a few months ago?)
  - download media
  - metadata?  Esp for yt clips
  - update mpd
  - add to mpd playlist: (scout_date_genre) config: naming pattern
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
import youtube_dl

from config import Config
import db
from messages import Messages
from utils import Utils, MPDClient

c = Config().conf_vars()
d = db.Database()
ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

class Musicscout():
  def __init__(self):
    ut = Utils()
    ut.symlink_musicdir()
    ut.clear_cache()

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
        genre = line[1].strip()
      except:
        genre = ''
      if line[0]:
        d.add_url(line[0])
        feeds += [[line[0],genre]]
    feedfile.close()
    print(feeds)
    return feeds

  def get_pages(self, feeds):
    for f in feeds:
      posts = feedparser.parse(f)
      for p in posts.entries:
        print(p)
        Database.check_url(f)
        posts = feedparser.parse(f)
        date = posts.entries[0].updated_parsed
        now = datetime.now()
        post_time = datetime.fromtimestamp(mktime(date))

  def grab_media_links(self, page):
    if 'youtu' in page:
      grab_yt(page)
    else:
      r = BeautifulSoup(get(page).content, 'lxml')
      frames = r.find_all('iframe')
      for f in frames:
        link = f['src']
        print(link)

  def download_all(self, link):
    batchdir = create_batch_dir()
    ydl_opts = {
        'outtmpl' : batchdir+'/%(title)s_%(id)s.%(ext)s',
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

"""
    """
