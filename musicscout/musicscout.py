#!/usr/bin/python3

"""
  TODO:
  - GOOGLE RECAPTCHA
  - add/rm from db
  - for each url, get all media more recent than last_updated (or cutoff of a few months ago?) Set last_updated as last function in loop so incomplete donwloads can restart
  - download media if < 10 min
  - metadata?  Esp for yt clips
  - update mpd
  - add to mpd playlists: (scout_genre, and scout_genre_new [or scout_genre_date?]) config: naming pattern
  - exit after updating media from feeds
  - log
  - add url to metadata?
"""

import os
import re
import shutil
import sys
import time

from bs4 import BeautifulSoup
import configparser
import datetime
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
        feed = line[0]
        d.add_url(feed)
        feeds += [[feed,genre]]
        self.get_media_links(feed, genre)
        timestamp = datetime.datetime.now()
        d.updated(feed,timestamp)
    feedfile.close()
    return feeds

  def get_media_links(self, feed, genre):
    """ get posts for a feed, strip media links  """
    posts = feedparser.parse(feed)
    genre_dir = Config().build_dirs(os.path.join(c['cache_dir'], genre))
    media_sites = ['youtu', 'bandcamp', 'soundcloud']
    for p in posts.entries:
      r = BeautifulSoup(requests.get(p.link).content, 'lxml')
      frames = r.find_all('iframe')
      for f in frames:
        try:
          link = f['src']
          f_link = ut.format_link(link) 
          check_song = d.check_song(f_link)
          if check_song and any(m in f_link for m in media_sites):
            self.yt_dl(link,genre)
            add_song = d.add_song(f_link)
            print("Downloaded: {} ".format(link))
          else:
            print("Did not dl: {} ".format(f_link))
        except:
          print("Non-working link: {}".format(f))
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
