from .exceptions import ExitException, OpenBookException
from .tableview import TableView
from .deletedialog import DeleteDialog
import datetime
import os
import logging

from typing import Dict, Any

class BookView(TableView):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

        try: book_dirs = filter(lambda f: f.is_dir(), os.scandir(config['notedir']))
        except FileNotFoundError: pass
        else:
            self.content = [[
                book_dir.name,
                str(len(os.listdir(book_dir))),
                datetime.datetime.fromtimestamp(os.stat(book_dir).st_atime_ns/1_000_000_000).strftime(config['dateformat']),
                datetime.datetime.fromtimestamp(os.stat(book_dir).st_mtime_ns/1_000_000_000).strftime(config['dateformat'])] for book_dir in book_dirs]

        self.empty_content_message = ['No notebooks detected.', 'Hit n to make one!']
        self.headers = ['BOOK TITLE (F1)  ', 'NOTES (F2)  ', 'OPENED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        self.keys = [
                lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, config['dateformat']),
                lambda datestr:datetime.datetime.strptime(datestr, config['dateformat']) ]
        super().__init__()
    
    def new(self, name: str):
        os.makedirs(os.path.join(self.config['notedir'], name))
        raise OpenBookException(name)

    def rename(self, row: int, new_name: str):
        os.rename(os.path.join(self.config['notedir'], self.content[row][0]), os.path.join(self.config['notedir'], new_name))
        self.content[row][0] = new_name

    def show_delete_dialog(self, row: int):
        self.delete_dialog = DeleteDialog([f'Are you sure you want to delete book "{self.content[row][0]}"?', 'This cannot be undone.'])

    def delete(self, row: int):
        pass

    def draw(self, stdscr):
        stdscr.move(0,0)
        stdscr.clrtoeol()
        super().draw(stdscr)

    def on_enter(self, row):
        title = self.content[self.real_selected][0]
        raise OpenBookException(title)

    def on_escape(self):
        raise ExitException
