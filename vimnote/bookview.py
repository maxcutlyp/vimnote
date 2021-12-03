from .exceptions import ExitException
from .tableview import TableView
from .random_content import content
import datetime

from typing import Callable

class BookView(TableView):
    def __init__(self, note_dir: str, open_book: Callable[[str],None] = lambda _:None):
        # TODO: convert note_dir to content here
        self.open_book = open_book

        self.content = content
        self.headers = ['BOOK TITLE (F1)  ', 'NOTES (F2)  ', 'CREATED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        self.keys = [
                lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y'),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y') ]
        super().__init__()
    
    def new(self, name: str):
        # create directory, open as book
        pass

    def draw(self, stdscr):
        stdscr.move(0,0)
        stdscr.clrtoeol()
        super().draw(stdscr)

    def on_enter(self, row):
        title = self.content[self.real_selected][0]
        self.open_book(title)

    def on_escape(self):
        raise ExitException
