"""
musicscout
Get media files from an updated list of music blogs

Config file at: ~/.config/musicscout/config

Usage:
  musicscout
  musicscout (-h | --help)
  musicscout (--version)

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
"""

""" Code:
Gregory Parrish
    http://github.com/greggparrish
"""

import os
from docopt import docopt

from musicscout import Musicscout



if __name__ == '__main__':
    arguments = docopt(__doc__, version='musicscout 1.0')
    try:
        with Musicscout() as ms:
            ms.get_feed_urls()
    except Exception as e:
        print('ERROR: {}'.format(e))
