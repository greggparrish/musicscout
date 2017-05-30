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

    if last_update:
      lu = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
    try:
      ft = datetime.datetime.fromtimestamp(mktime(posts.feed.updated_parsed))
    except:
      ft = None

    ''' IF FEED HAS BEEN UPDATED SINCE LAST CHECK '''

    if not lu or not ft or ft > lu:
      for p in posts.entries:
        pt = datetime.datetime.fromtimestamp(mktime(p.updated_parsed))
        ''' IF INDIVIDUAL POST IS NEWER THAN LAST UPDATE '''
        if ft == None or pt > lu:
          if 'reddit' in feed:
            links = ut.reddit_links(p)
          elif 'tumblr' in feed:
            links = ut.tumblr_links(p)
          else:
            links = ut.blog_links(p)
          for l in links:
            check_song = d.check_song(l)
            media_sites = ['youtu', 'bandcamp.com', 'soundcloud', 'redditmedia']
            if not check_song and any(m in l for m in media_sites):
              dl = self.yt_dl(l,genre)
              if 'youtu' in l and dl != '':
                ut.add_metadata(dl, l, genre)
              add_song = d.add_song(l)

    ft = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return ft

  def yt_dl(self, link, genre):
    genre_dir = os.path.join(c['cache_dir'],genre)
    ydl_opts = {
        'restrict_filenames': True,
        'outtmpl' : genre_dir+'/%(title)s__%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'get_filename': True,
        'max_downloads': '3',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
          }],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      try:
        vidinfo = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(vidinfo)
        base = '.'.join(filename.split('.')[:-1])
        filename = "{}.mp3".format(base)
        print("  ** DOWNLOADING: {} from {}".format(vidinfo.get('title', None), link))
      except:
        filename = ''
        print("Unable to download {}".format(link))
    return filename

ms = Musicscout()
ms.get_urls()
ut.clean_cache()
mpd_update()
sleep(10)
make_playlists()
