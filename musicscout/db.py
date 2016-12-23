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
      c.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, last_update TIMESTAMP)')
      c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE)')

  def updated(self, feed, timestamp):
    """ update url with last time updated """
    with dbconn(feeds_db) as c:
      url = c.execute("UPDATE feeds SET last_update=? where url = ?", (timestamp,feed,))

  def add_url(self,feed):
    """ add url to db """
    with dbconn(feeds_db) as c:
      url = c.execute("INSERT OR IGNORE INTO feeds (url) VALUES(?)", (feed,))

  def update_time(self, url):
    """ check db for last time a feed was updated """
    with dbconn(feeds_db) as c:
      feed_date = c.execute("SELECT last_update FROM feeds WHERE url = ?", (url,)).fetchone()
      return feed_date

  def check_song(self, track):
    """ check db for a track """
    with dbconn(feeds_db) as c:
      song = c.execute("SELECT url FROM songs WHERE url = ?", (track,)).fetchone()
      return song

  def add_song(self, track):
    """ add url to db """
    with dbconn(feeds_db) as c:
      song = c.execute("INSERT OR IGNORE INTO songs (url) VALUES(?)", (track,))

