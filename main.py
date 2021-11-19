#!/usr/bin/env python3.10

from vimnote.bookview import BookView
from vimnote.config import get_config
import sys
import os
import curses
import logging

from typing import List, Any

CONFIG = get_config(os.path.expanduser('~/.config/vimnoterc'))

def main(stdscr):
    stdscr.clear()
    curses.curs_set(False)
    curses.use_default_colors()
    stdscr.refresh() # required for some reason, otherwise doesn't refresh until first keypress

    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    tv = BookView(CONFIG['notedir'])

    while True:
        tv.draw(stdscr)
        stdscr.refresh()

        # break on q, ^D (chr(4)), ^C (KeyboardInterrupt)
        try:
            if (key := stdscr.getch()) in (ord('q'), 4):
                break
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    curses.wrapper(main)
