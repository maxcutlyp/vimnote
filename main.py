#!/usr/bin/env python3.10

from vimnote.bookview import BookView
from vimnote.noteview import NoteView
from vimnote.tableview import TableView
from vimnote.config import get_config
from vimnote.exceptions import ExitException
import sys
import os
import curses
import logging

from typing import List, Any

CONFIG = get_config(os.path.expanduser('~/.config/vimnoterc'))
view: TableView = None

def open_book(title: str):
    global view
    view = NoteView(CONFIG['notedir'], title, close_book=close_book)

def close_book():
    global view
    view = BookView(CONFIG['notedir'], open_book=open_book)

def main(stdscr):
    global view
    stdscr.clear()
    curses.curs_set(False)
    curses.use_default_colors()
    stdscr.refresh() # required for some reason, otherwise doesn't refresh until first keypress

    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    close_book() # open BookView

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

if __name__ == '__main__':
    os.environ['ESCDELAY'] = '25' # avoid long delay after hitting escape
    curses.wrapper(main)
