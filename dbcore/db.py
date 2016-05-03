#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import sqlite3
import os

config_path = os.path.join(os.path.expanduser('~'), '.config/musicscout/')
feeds_db =  os.path.join(config_path, 'feeds.db')

class Database:
  def __init__(self):
    global conn
    global c
    conn = sqlite3.connect(feeds_db)
    c = conn.cursor()
    Database._create_table()
    conn.close()

  def _create_table():
    c.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, url TEXT UNIQUE)')
    conn.commit()

  def check_url(feed):
    conn = sqlite3.connect(feeds_db)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO feeds(url) VALUES('%s')" % (feed))
    url_id = c.execute("SELECT id FROM feeds WHERE url = ('%s')" % (feed))
    conn.commit()
    feed_id = url_id.fetchone()[0]

