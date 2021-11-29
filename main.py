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

    view = BookView(CONFIG['notedir'])

    while True:
        view.draw(stdscr)
        stdscr.refresh()

        # break on q, ^D (chr(4)), ^C (KeyboardInterrupt)
        kills = (ord('q'), 4) if not view.is_searching else (4,)
        try:
            if (key := stdscr.getch()) in kills:
                break
        except KeyboardInterrupt:
            break
        
        # else let the view handle it
        view.handle_keypress(key)

if __name__ == '__main__':
    os.environ['ESCDELAY'] = '25' # avoid long delay after hitting escape
    curses.wrapper(main)
