#!/usr/bin/python3

"""
musicscout
Get media files from an updated list of music blogs

Config file at: ~/.config/musicscout/config

Usage:
  musicscout
  musicscout <tag>
  musicscout (-h | --help)
  musicscout (--version)

Options:
  -t --tag                  Search tag
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

def main():
  arguments = docopt(__doc__, version='musicscout 1.0')
  ms = Musicscout()

if __name__ == '__main__':
    main()


