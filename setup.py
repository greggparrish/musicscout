#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import, print_function

import os
import sys
import subprocess
import shutil
from setuptools import setup


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    return open(path).read()


def build_manpages():
    # Go into the docs directory and build the manpage.
    docdir = os.path.join(os.path.dirname(__file__), 'docs')
    curdir = os.getcwd()
    os.chdir(docdir)
    try:
        subprocess.check_call(['make', 'man'])
    except OSError:
        print("Could not build manpages (make man failed)!", file=sys.stderr)
        return
    finally:
        os.chdir(curdir)

    # Copy resulting manpages.
    mandir = os.path.join(os.path.dirname(__file__), 'man')
    if os.path.exists(mandir):
        shutil.rmtree(mandir)
    shutil.copytree(os.path.join(docdir, '_build', 'man'), mandir)

# Build manpages if we're making a source distribution tarball.
if 'sdist' in sys.argv:
    build_manpages()

setup(
    name='musicscout',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    license='',
    platforms='',
    long_description=_read('README.rst'),
    test_suite='test.testall.suite',
    include_package_data=True,  # Install plugin resources.

    packages=[
        'musicscout',
        'musicscout.ui',
        'musicscout.util',
        'musicscout.dbcore',
    ],
    entry_points={
        'console_scripts': [
            'beet = musicscout.ui:main',
        ],
    },

    install_requires=[
        'beautifulsoup4',
        'enum34>=1.0.4',
        'jellyfish',
        'munkres',
        'python-mpd2',
        'pyyaml',
        'unidecode',
        'youtube-dl',
    ] + (['colorama'] if (sys.platform == 'win32') else []) +
        (['ordereddict'] if sys.version_info < (2, 7, 0) else []),

    tests_require=[
        'flask',
        'mock',
        'pyechonest',
        'pylast',
        'rarfile',
        'responses',
        'pyxdg',
        'pathlib',
    ],

    # Plugin (optional) dependencies:
    extras_require={
    },
    # Non-Python/non-PyPI plugin dependencies:
    # convert: ffmpeg
    # bpd: pygst

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
