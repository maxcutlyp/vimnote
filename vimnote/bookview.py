from .exceptions import ExitException, OpenBookException
from .tableview import TableView
from .random_content import content
import datetime

from typing import Callable

class BookView(TableView):
    def __init__(self, note_dir: str):
        # TODO: convert note_dir to content here

        self.empty_content_message = ['No notebooks detected.', 'Hit n to make one!']
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
        raise OpenBookException(title)

    def on_escape(self):
        raise ExitException
