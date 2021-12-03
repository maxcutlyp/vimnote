from .tableview import TableView
from .random_content import content
from .exceptions import CloseBookException
import datetime

from typing import Callable

class NoteView(TableView):
    def __init__(self, note_dir: str, book: str):
        # TODO: convert note_dir and book to content here
        self.book = book

        self.empty_content_message = ['No notes detected.', 'Hit n to make one!']
        self.headers = ['NOTE TITLE (F1)  ', 'LINES (F2)  ', 'CREATED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        self.keys = [
                lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y'),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y') ]
        super().__init__()

    def draw(self, stdscr):
        stdscr.addstr(0,0, f'Book: {self.book}')
        stdscr.clrtoeol()
        super().draw(stdscr)

    def on_enter(self, row):
        pass # TODO: spawn vim instance corresponding to selected note

    def on_escape(self):
        raise CloseBookException
