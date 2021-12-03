#!/usr/bin/env python3.10

from vimnote.bookview import BookView
from vimnote.noteview import NoteView
from vimnote.tableview import TableView
from vimnote.config import get_config
from vimnote.exceptions import ExitException, OpenBookException, CloseBookException
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

    view = BookView(CONFIG)

    while True:
        view.draw(stdscr)
        stdscr.refresh()

        # break on keyboard interrupt or if ExitException is raised by view
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break
        
        # else let the view handle it
        try: view.handle_keypress(key)
        except ExitException: break
        except OpenBookException as e:
            stdscr.clear()
            stdscr.refresh()
            view = NoteView(CONFIG, e.title)
        except CloseBookException:
            stdscr.clear()
            stdscr.refresh()
            view = BookView(CONFIG)

if __name__ == '__main__':
    os.environ['ESCDELAY'] = '25' # avoid long delay after hitting escape
    curses.wrapper(main)
