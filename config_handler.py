import configparser
from distutils.command.config import config

config = configparser.ConfigParser()
config.read('conf.ini')

sqlite_path = config['sqlite configuration']['path']

def get_sqlite_path():
    return sqlite_path
