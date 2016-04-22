import configparser

def createConfig(path):
    """
    Create a config file
    """
    config = ConfigParser.ConfigParser()
    with open(path, "wb") as config_file:
        config.write(config_file)
