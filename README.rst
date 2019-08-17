ABOUT
-----
Musicscout is an RSS reader for music blogs that downloads the media files listed in blog posts (youtube, soundcloud, bandcamp), organizes them into genre folders, and loads them into MPD playlists named after the genre.

The app doesn't currently delete old files from the cache, so you'll need to clean it out periodically or it could grow quite large.

**Please support the artists and blogs.**


REQUIRES
--------
- **Python 3.6**
- ffmpeg or avconv
- MPD

INSTALL
-------
- wget https://github.com/greggparrish/musicscout/archive/master.tar.gz -O musicscout.tar.gz 
- pip install musicscout.tar.gz 

CONFIG
------
- config file: ~/.config/musicscout/config
- set mpd host, port, and music directory
- set cache (dir for mp3s), default: ~/.config/musicscout/musicscout_cache
- set url file: url | genre (see [urls_example](https://github.com/greggparrish/musicscout/blob/master/urls_example) in repo)

USAGE
-----
- musicscout
- (if you get download errors, try updating [youtube-dl](https://github.com/ytdl-org/youtube-dl))
