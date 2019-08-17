import os
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit("Musicscout requires python >= 3.6")

version = '1.80'

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='musicscout',
    version=version,
    description='Musicscout downloads media from music blogs.',
    long_description=open('README.rst').read(),
    author='Gregory Parrish',
    author_email='me@greggparrish.com',
    license='Unlicense',
    keywords=['music', 'genres', 'music blogs', 'cli', 'mpd'],
    url='http://github.com/greggparrish/musicscout',
    packages=find_packages(),
    package_data={},
    install_requires=required,
    entry_points={
        'console_scripts': [
            'musicscout=musicscout.__main__:main',
        ],
    },
)
