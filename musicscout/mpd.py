#!/usr/bin/python3

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
  def symlink_musicdir(self):
    """ Cache has to be within mpd music dir to load tracks,
        so symlink it if user didn't choose a path already in
        their mpd music dir """
    try:
      rel_path = cf['cache_dir'].split('/')[-1]
      os.symlink(cf['cache_dir'],os.path.join(cf['music_dir'],rel_path))
    except FileExistsError:
      pass

  def add_song(song):
    with MPDConn(c['mpd_host'],c['mpd_port']) as m:
      m.update('cache')
      sleep(3)
      song_id = m.add(song)
      play_state = m.status()['state']
      if play_state is not 'play':
        m.play()

