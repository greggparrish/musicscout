#!/usr/bin/python3

import datetime
import logging
import os
import re
from time import mktime, sleep


import feedparser
import youtube_dl

from config import Config
import db
from utils import Utils
from mpdutil import mpd_update, make_playlists

c = Config().conf_vars()
db = db.Database()
ut = Utils()
ConfigPath = os.path.join(os.path.expanduser('~'), '.config/musicscout/')
logging.basicConfig( filename=ConfigPath + 'scout.log', format='%(message)s', level=logging.INFO)
media_sites = [ 'youtu', 'bandcamp.com', 'soundcloud', 'redditmedia']


class Musicscout():
    def __init__(self):
        self.dlcount = 0

    def __enter__(self):
        ''' Symlink download dir to mpd dir if not already, start log '''
        ut.symlink_musicdir()
        logging.info("\n### INIT: SCOUT RUN ON: {}".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return self

    def __exit__(self, exc_class, exc, traceback):
        ''' Rm partial dls, update mpd, build playlists, end log '''
        ut.clean_cache()
        mpd_update()
        sleep(10)
        make_playlists()
        logging.info("### DL TOTAL: {}".format(self.dlcount))
        logging.info("### END: SCOUT RUN ON: {}".format( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return True

    def compare_feed_date(self, lu, posts):
        ''' Check if site feed is newer than last scout run
        to avoid unnecessary updates '''
        try:
            ft = datetime.datetime.fromtimestamp(mktime(posts.feed.updated_parsed))
            if not lu or not ft or ft > lu:
                return ft
            else:
                return False
        except:
            return False

    def get_feed_urls(self):
        ''' Open urls file in .config, make list of feeds '''
        feeds = []
        feedfile = open(ConfigPath + 'urls')
        for line in feedfile:
            line = line.strip()
            if not line.startswith("#"):
                line = line.replace('\n', '').strip()
                line = line.split('|')
                try:
                    genre = re.sub( r'[-\s]+', '-', (re.sub( r'[^\w\s-]', '', line[1]).strip().lower()))
                except:
                    genre = 'uncategorized'
                if line[0]:
                    feed = line[0].strip()
                    db.add_url(feed)
                    feeds += [[feed, genre]]
                    self.get_media_links(feed, genre)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.update_time(feed, now)
        feedfile.close()
        return True

    def get_media_links(self, feed, genre):
        ''' Get posts for a feed, strip media links from posts '''
        print("  ** FEED: checking posts for {}".format(feed))
        links = []
        posts = feedparser.parse(feed)
        last_update = db.feed_time(feed)[0]
        if last_update != None:
            try:
                lu = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
            except:
                lu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            lu = None
        ft = self.compare_feed_date(lu, posts)
        if ft != False:
            for p in posts.entries:
                pt = datetime.datetime.fromtimestamp(mktime(p.updated_parsed))
                if ft is None or lu is None or pt > lu:
                    if 'reddit' in feed:
                        links = ut.reddit_links(p)
                    elif 'tumblr' in feed:
                        links = ut.tumblr_links(p)
                    else:
                        links = ut.blog_links(p)
                    if links:
                        self.download_new_media(links, genre)
        return ft

    def download_new_media(self, links, genre):
        for l in links:
            if any(m in l for m in media_sites):
                check_song = db.check_song(l)
                if not check_song:
                    dl = self.yt_dl(l, genre)
                    if 'youtu' in l and dl != False:
                        ut.add_metadata(dl, l, genre)
                    add_song = db.add_song(l)
                    self.dlcount += 1
        return True

    def yt_dl(self, link, genre):
        genre_dir = os.path.join(c['cache_dir'], genre)
        ydl_opts = {
            'restrict_filenames': True,
            'outtmpl': genre_dir + '/%(title)s__%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'get_filename': True,
            'max_downloads': '3',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                vidinfo = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(vidinfo)
                base = '.'.join(filename.split('.')[:-1])
                filename = "{}.mp3".format(base)
                vidtitle = vidinfo.get('title', None)
                logging.info( "    ** DL: {} from {}".format(vidtitle, link))
                print("  ** DL: {} from {}".format(vidtitle, link))
                return filename
            except Exception as e:
                logging.info( "    ** FAILED: {} {}".format(link, e))
                print("  ** FAILED: {} {}".format(link, e))
                return False

if __name__ == '__main__':
    try:
        with Musicscout() as ms:
            ms.get_feed_urls()
    except Exception as e:
        print('ERROR: {}'.format(e))
