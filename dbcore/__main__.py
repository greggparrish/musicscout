#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import os

ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

feedsdb =  os.path.join(ConfigPath, 'feeds.db')

conn = sqlite3.connect(feedsdb)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, date date, url text)''')
conn.commit
conn.close()


