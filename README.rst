ABOUT
-----
Musicscout is an RSS reader for music blogs that downloads the media files listed in blog posts (youtube, soundcloud, bandcamp), organizes them into genre folders, and loads them into MPD playlists named after the genre.

The app doesn't currently delete old files from the cache, so you'll need to clean it out periodically or it could grow quite large. 

**Please support both the artists and music blogs.**


REQUIRES
--------
- Python 3
- MPD

INSTALL
-------
- Download zip
- unzip musicscout-master.zip
- cd musicscout-master
- pip3 install -r requirements.txt

CONFIG
------
- config file: ~/.config/musicscout/config
- set cache (dir for mp3s), default: ~/,config/musicscout/musicscout_cache
- set url file: url | genre (see example in repo)
- set mpd host, port, and music directory

USAGE
-----
- python3 musicscout

