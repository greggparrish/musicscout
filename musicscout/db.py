#!/usr/bin/python3

import sqlite3
import os

config_path = os.path.join(os.path.expanduser('~'), '.config/musicscout/')
feeds_db =  os.path.join(config_path, 'feeds.db')

class dbconn(object):
    """ DB context manager """
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()

class Database:
  def __init__(self):
    self._create_table()

  def _create_table(self):
    with dbconn(feeds_db) as c:
      c.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, last_update DATE)')

  def add_url(self,feed):
    """ add url to db """
    with dbconn(feeds_db) as c:
      added = c.execute("INSERT OR IGNORE INTO feeds (url) VALUES(?)", (feed,))
    return added

  def check_url():
    """ get all urls """
    with dbconn(feeds_db) as c:
      feeds = c.execute("SELECT url FROM feeds").fetchall()
    return feeds
