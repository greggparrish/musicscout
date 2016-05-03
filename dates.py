#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
- Need to add db, or possibly just flat file listing last time each url was dled
- Consider using article title as song title
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import configparser
import feedparser
import os
import re
from requests import get
import shutil
import sys
from time import mktime
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import youtube_dl

from dbcore.db import *

ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

def config():
  config = configparser.ConfigParser()
  config.read(ConfigPath+'config')
  storage_dir = config['storage']['save_to']
  if '~' in storage_dir:
    storage_dir = os.path.expanduser(storage_dir)
  return storage_dir

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

feeds = get_urls()
for f in feeds:
  '''
  get most recent post
  '''
  Database.check_url(f)
  posts = feedparser.parse(f)
  date = posts.entries[0].updated_parsed
  now = datetime.now()
  post_time = datetime.fromtimestamp(mktime(date))

