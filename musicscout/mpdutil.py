#!/usr/bin/python3

from mpd import MPDClient
from config import Config

c = Config().conf_vars()

class MPDConn(object):
  def __init__(self, host, path):
    self.host = c['mpd_host']
    self.port = c['mpd_port']
    self.client = None

  def __enter__(self):
    self.client = MPDClient()
    self.client.connect(c['mpd_host'],c['mpd_port'])
    # 0 is random off, 1 is on
    #self.client.random(0)
    return self.client

  def __exit__(self, exc_class, exc, traceback):
    self.client.close()
    self.client.disconnect()

def mpd_update():
  rel_path = c['cache_dir'].split('/')[-1]
  with MPDConn(c['mpd_host'],c['mpd_port']) as m:
    m.update(rel_path)
