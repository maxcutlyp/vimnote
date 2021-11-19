from .tableview import TableView

class BookView(TableView):
    def __init__(self, note_dir: str):
        # TODO: convert note_dir to content here
        content = [['abcabc', '123', '01 November 2021', '11 November 2021']]*100
        super().__init__(content)

    def draw(self, stdscr):
        # todo: add header info
        super().draw(stdscr)
