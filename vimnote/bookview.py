from .tableview import TableView

class BookView(TableView):
    def __init__(self, note_dir: str):
        # TODO: convert note_dir to content here
        content = [['abcabc', '123', '01 November 2021', '11 November 2021']]*100
        headers = ['BOOK TITLE (F1)  ', 'NOTES (F2)  ', 'CREATED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        super().__init__(content, headers)

    def draw(self, stdscr):
        # todo: add header info
        super().draw(stdscr)
