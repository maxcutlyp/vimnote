from .tableview import TableView
from .random_content import content
import datetime

class NoteView(TableView):
    def __init__(self, note_dir: str, book: str):
        # TODO: convert note_dir and book to content here
        headers = ['NOTE TITLE (F1)  ', 'LINES (F2)  ', 'CREATED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        keys = [lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y'),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y')]
        super().__init__(content, headers, keys)

    def draw(self, stdscr):
        # TODO: add current book
        super().draw(stdscr)

