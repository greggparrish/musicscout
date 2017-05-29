#!/usr/bin/python3

from bs4 import BeautifulSoup
import datetime
import os
import re
import requests
import time

from mutagen import File
from mutagen.id3 import ID3NoHeaderError
from mutagen.easyid3 import EasyID3

from config import Config
import db
from messages import Messages

cf = Config().conf_vars()

class Utils:
  def symlink_musicdir(self):
    """ Cache has to be within mpd music dir to load tracks,
        so symlink it if user didn't choose a path already in
        their mpd music dir """
    try:
      rel_path = cf['cache_dir'].split('/')[-1]
      os.symlink(cf['cache_dir'],os.path.join(cf['music_dir'],rel_path))
    except FileExistsError:
      pass

  def create_dir(self, path):
    """ Used to create intial dirs, and genre dirs within cache """
    if not os.path.exists(path):
      os.makedirs(path)
    return path

  def clean_cache(self):
    for root, subFolders, files in os.walk(cf['cache_dir']):
      for file in files:
        if '.part' in file:
          os.remove(os.path.join(root,file))

  def format_link(self,link):
    if 'recaptcha' or 'widgets.wp.com' in link:
      fl = False
    if 'youtu' in link:
      fl = link.split('?')[0]
    if 'soundcloud' in link:
      fl = link.split('&')[0]
    if 'redditmedia' in link:
      fl = "https:"+link
    return fl.strip()

  def reddit_links(self, p):
    links = []
    media_sites = ['youtu', 'bandcamp.com', 'soundcloud']
    ll = BeautifulSoup(p['content'][0]['value'], 'lxml')
    for l in ll.find_all('a'):
      if any(m in l.get('href') for m in media_sites):
        links.append(l.get('href'))
    return links

  def tumblr_links(self, p):
    links = []
    r = BeautifulSoup(p['summary'], 'lxml')
    frames = r.find_all('iframe')
    for f in frames:
      src = f.get('src')
      if src:
        links.append(f.get('src'))
    return links

  def blog_links(self, p):
    links = []
    r = BeautifulSoup(requests.get(p.link).content, 'lxml')
    media_sites = ['youtu', 'bandcamp.com', 'soundcloud']
    frames = r.find_all('iframe')
    for f in frames:
      if 'src' in f and any(m in f['src'] for m in media_sites):
        try:
          if 'bandcamp' in f['src']:
            fl = re.search(r'href=[\'"]?([^\'" >]+)', str(f))
            if fl:
              links.append(fl.group(1))
          else:
            links.append(self.format_link(f['src']))
        except requests.exceptions.RequestException as e:
          print(e)
    return links

  def add_metadata(self, path, link, genre):
    fn = path.split('/')[-1]
    vi = fn.split('__')[0]
    vidinfo = re.sub("[\(\[].*?[\)\]]", "", vi)
    if '-' in vidinfo:
      artist = vidinfo.split('-')[0]
      fulltitle = vidinfo.split('-')[1]
      title = fulltitle.split('__')[0]
    else:
      title = vidinfo
      artist = ''
    if '?' in link:
      link = link.split('?')[0]
    try:
      song = EasyID3(path)
    except ID3NoHeaderError:
      song = File(path, easy=True)
    song['title'] = title
    song['artist'] = artist
    song['genre'] = genre
    song['website'] = link
    song.save()

