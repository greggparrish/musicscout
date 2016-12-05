#!/usr/bin/python3

import datetime
import os
import re
import time
import webbrowser

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

  def format_link(self,link):
    if 'recaptcha' or 'widgets.wp.com' in link:
      fl = False
    if 'youtu' in link:
      fl = link.split('?')[0]
    if 'soundcloud' in link:
      fl = link.split('&')[0]
    return fl

