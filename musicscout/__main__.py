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
    https://github.com/greggparrish/musicscout
"""

import os
import argparse

from musicscout import Musicscout

if __name__ == '__main__':
    p=argparse.ArgumentParser(description='Get media files from an updated list of music blogs.')
    p.add_argument('-v', '--version', action='version', version='musicscout v. 1.10')
    args=p.parse_args()

    try:
        with Musicscout() as ms:
            ms.get_feed_urls()
    except Exception as e:
        print(f'ERROR: {e}')
