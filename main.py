#!/usr/bin/env python3.10

from vimnote.listview import ListView
import sys
import os
import configparser

from typing import List

CONFIG = get_config(os.path.expanduser('~/.config/vimnoterc'))

def main(args: List[str]):
    lv = ListView()

def get_config(path: str):
    pass

if __name__ == '__main__':
    main(sys.argv[1:])
