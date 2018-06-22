import logging
import os

from mpd import MPDClient
from config import Config

c = Config().conf_vars()
logging.getLogger("mpd").setLevel(logging.WARNING)


class MPDConn:
    def __init__(self, host, path):
        self.host = c['mpd_host']
        self.port = c['mpd_port']
        self.client = None

    def __enter__(self):
        self.client = MPDClient()
        self.client.connect(c['mpd_host'], c['mpd_port'])
        # 0 is random off, 1 is on
        # self.client.random(0)
        return self.client

    def __exit__(self, exc_class, exc, traceback):
        self.client.close()
        self.client.disconnect()


def mpd_update():
    rel_path = c['cache_dir'].split('/')[-1]
    with MPDConn(c['mpd_host'], c['mpd_port']) as m:
        m.update(rel_path)


def make_playlists():
    cachedir = c['cache_dir']
    with MPDConn(c['mpd_host'], c['mpd_port']) as m:
        for g in list(os.walk(cachedir))[1:]:
            genre = g[0].split('/')[-1]
            playlist = f"musicscout_{genre}"
            try:
                m.playlistclear(playlist)
            except Exception as e:
                pass
            for s in g[2]:
                try:
                    song = os.path.join(cachedir.split('/')[-1], genre, s)
                    m.playlistadd(playlist, song)
                except BaseException:
                    pass
