import os
import configparser

confp = configparser.ConfigParser()
conf_path = 'config/config.ini'


def get_config():
    if not os.path.exists(conf_path):
        raise FileNotFoundError()
    confp.read(conf_path, encoding='utf-8')
    d = confp['DEFAULT']
    conf = {
        'version': d.get('version'),
        'prefix': d.get('prefix'),
        'discord_bot_key': d.get('discord_bot_key'),
        'activity_name': d.get('activity_name'),
        'debug': d.getboolean('debug')
    }
    return conf
