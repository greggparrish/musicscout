#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup
import configparser
import feedparser
import os
import re
from requests import get
import shutil
import sys
import time
from urllib.parse import urlparse, parse_qs
import youtube_dl

ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

def config():
  config = configparser.ConfigParser()
  config.read(ConfigPath+'config')
  storage_dir = config['storage']['save_to']
  if '~' in storage_dir:
     storage_dir = os.path.expanduser(storage_dir)
  return storage_dir

def create_storage_dir():
  sd = config()
  if not os.path.exists(sd):
    os.makedirs(sd)

def create_batch_dir():
  sd = config()
  nowtime = time.strftime("%b_%d_%Y")
  batchdir = os.path.join(sd, 'music_for_'+nowtime)
  if not os.path.exists(batchdir):
    os.makedirs(batchdir)
  return batchdir

def get_urls():
  """
  Open urls file in .config, make list
  """
  feeds = []
  feedfile = open(ConfigPath+'urls')
  for line in feedfile:
    line = line.rstrip()
    if not line or line.startswith('#'):
      continue
    feeds.append(line)
  feedfile.close()
  return feeds

def grab_media_links(page):
  r = BeautifulSoup(get(page).content, 'lxml')
  frames = r.find_all('iframe')
  for f in frames:
    link = f['src']
    if 'youtu' in link:
      grab_yt(link)
    elif 'soundcloud' in link:
      grab_sc(link)
    elif 'bandcamp' in link:
      grab_bc(link)
    elif 'vimeo' in link:
      grab_vm(link)

def grab_vm(link):
  download_all(link)

def grab_sc(link):
  download_all(link)

def grab_yt(link):
  download_all(link)

def grab_bc(link):
  download_all(link)

def download_all(link):
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

def get_yt_video_id(url):
  """Returns Video_ID extracting from the given url of Youtube
  """
  if url.startswith(('youtu', 'www')):
    url = 'http://' + url
  query = urlparse(url)
  if 'youtube' in query.hostname:
    if query.path == '/watch':
      return parse_qs(query.query)['v'][0]
    elif query.path.startswith(('/embed/', '/v/')):
      return query.path.split('/')[2]
  elif 'youtu.be' in query.hostname:
    return query.path[1:]
  else:
    raise ValueError


feeds = get_urls()
for f in feeds:
  posts = feedparser.parse(f)
  for p in posts.entries:
    grab_media_links(p.link)
