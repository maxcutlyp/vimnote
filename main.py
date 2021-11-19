#!/usr/bin/env python3.10

from vimnote.tableview import TableView
from vimnote.config import get_config
import sys
import os

from typing import List

CONFIG = get_config(os.path.expanduser('~/.config/vimnoterc'))

def main(args: List[str]):
    print(CONFIG)
    tv = TableView(None)

if __name__ == '__main__':
    main(sys.argv[1:])
