#!/usr/bin/env python3.10

from vimnote.tableview import TableView
import sys
import os
import configparser

from typing import List

def get_config(path: str):
    # config file doesn't have sections but parser requires sections
    # so just add a default section after loading file
    try:
        f = open(path)
    except IOError:
        content = []
    else:
        with f:
            content = f.readlines()
    content.insert(0, '[DEFAULT]')
    cfg = configparser.ConfigParser()
    cfg.read_string('\n'.join(content))

    # configparser doesn't automatically guess the datatypes based on fallback value
    # so we create a list associating keys, getters, and fallbacks
    # and then use the parser to fill in what it can
    default = cfg['DEFAULT']
    options = [
            ('previewratio', default.getfloat, 0.5),
            ('confirmdelete', default.getboolean, True),
            ('notedir', default.get, '~/.vimnote/') ]
    return { key: getter(key, fallback=fallback) for (key, getter, fallback) in options }

CONFIG = get_config(os.path.expanduser('~/.config/vimnoterc'))

def main(args: List[str]):
    print(CONFIG)
    tv = TableView(None)

if __name__ == '__main__':
    main(sys.argv[1:])
