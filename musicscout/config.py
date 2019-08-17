import os
import configparser

CONFIGPATH = os.path.join(os.path.expanduser('~'), '.config/musicscout/')

''' read or create config file '''
conf = configparser.ConfigParser()


class Config:
    def __init__(self):
        self.build_dirs(CONFIGPATH)
        confvars = conf.read(os.path.join(CONFIGPATH, 'config'))
        if not confvars:
            self.create_config()
        cache_dir = self.conf_vars()['cache_dir']
        self.build_dirs(self.format_path(cache_dir))

    def build_dirs(self, path):
        """ Create musicscout dir and cache dir in .config """
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def conf_vars(self):
        conf_vars = {
            'browser': conf['browser']['browser'],
            'cache_dir': self.format_path(conf['storage']['cache']),
            'urls': self.format_path(conf['storage']['urls']),
            'mpd_host': conf['mpd']['host'],
            'mpd_port': conf['mpd']['port'],
            'music_dir': self.format_path(conf['mpd']['music_dir']),
        }
        return conf_vars

    def create_config(self):
        """ Create config file """
        print("No config file found at ~/.config/musicscout, using default settings. Creating file with defaults.")
        path = self.format_path(os.path.join(CONFIGPATH, 'config'))
        conf.add_section("storage")
        conf.set("storage", "cache", "~/.config/musicscout/musicscout_cache")
        conf.set("storage", "urls", "~/.config/musicscout/urls")
        conf.add_section("player")
        conf.set("player", "player", "mpd")
        conf.add_section("mpd")
        conf.set("mpd", "music_dir", "~/music")
        conf.set("mpd", "host", "localhost")
        conf.set("mpd", "port", "6600")
        conf.add_section("browser")
        conf.set("browser", "browser", "google-chrome")
        with open(path, "w") as config_file:
            conf.write(config_file)

    def create_urls(self):
        """ Create urls file """
        print("No urls file found at ~/.config/musicscout. Creating file, but you'll need to add rss feeds to it.")
        path = self.format_path(os.path.join(CONFIGPATH, 'urls'))
        with open(path, 'a') as url_file:
            url_file.write('# format: url | genre\n# http://www.post-punk.com/feed/ | postpunk\n# Check https://github.com/greggparrish/musicscout/blob/master/urls_example for more examples')
        return True

    def format_path(self, path):
        if '~' in path:
            path = os.path.expanduser(path)
        else:
            path = path
        return path
