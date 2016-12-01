#!/usr/bin/python3

import datetime
import os
import re
import time
import webbrowser

from mpd import MPDClient

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

  def browser(self,filename):
    """ Open browser with post url """
    wb = webbrowser.get(cf['browser']).open(post_url)
    return wb

  def clear_cache(self):
    """ Remove media from cache dir if older than a day """
    now_ts = int(time.time())
    files = [f for f in os.listdir(cf['cache_dir']) if os.path.isfile(os.path.join(cf['cache_dir'],f))]
    for f in files:
      ms_track = re.findall('MSCOUT_\d*_\d*_\d*.mp3', f)
      if ms_track:
        ts =  int(ms_track[0].split('_')[1])
        if ts+86400 < now_ts:
          os.remove(os.path.join(cf['cache_dir'],ms_track[0]))

class MPDConn(object):
  def __init__(self, host, path):
    self.host = c['mpd_host']
    self.port = c['mpd_port']
    self.client = None
    d = Database()

  def __enter__(self):
    self.client = MPDClient()
    self.client.connect(c['mpd_host'],c['mpd_port'])
    # 0 is random off, 1 is on
    #self.client.random(0)
    return self.client

  def __exit__(self, exc_class, exc, traceback):
    self.client.close()
    self.client.disconnect()

class MPDQueue(object):
  def add_song(song):
    with MPDConn(c['mpd_host'],c['mpd_port']) as m:
      m.update('cache')
      sleep(3)
      song_id = m.add(song)
      play_state = m.status()['state']
      if play_state is not 'play':
        m.play()
