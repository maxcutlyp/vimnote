from .tableview import TableView
from .random_content import content
import datetime

class BookView(TableView):
    def __init__(self, note_dir: str):
        # TODO: convert note_dir to content here
        headers = ['BOOK TITLE (F1)  ', 'NOTES (F2)  ', 'CREATED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        keys = [lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y'),
                lambda datestr:datetime.datetime.strptime(datestr, '%I:%M%p %m-%d-%Y')]
        super().__init__(content, headers, keys)
