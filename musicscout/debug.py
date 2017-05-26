#!/usr/bin/python3

import os
import re
from time import mktime,sleep


from bs4 import BeautifulSoup
import feedparser
import requests
import youtube_dl


posts = feedparser.parse('http://awakeonsundaynight.tumblr.com/rss')
media_sites = ['youtu', 'bandcamp.com', 'soundcloud']

for p in posts.entries:
  r = BeautifulSoup(p['summary'], 'lxml')
  frames = r.find_all('iframe')
  for f in frames: 
    src = f.get('src')
    if src:
      g = src.split('?')[0]
      print(g)

