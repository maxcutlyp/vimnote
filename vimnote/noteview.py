from .tableview import TableView
from .exceptions import CloseBookException, EditNoteException
from .deletedialog import DeleteDialog
import datetime
import os

from typing import Dict, Any

class NoteView(TableView):
    def __init__(self, config: Dict[str, Any], book: str):
        # TODO: convert note_dir and book to content here
        self.book = book
        self.config = config

        try: note_files = filter(lambda f: os.path.splitext(f)[1] == '.vmnt', os.scandir(os.path.join(config['notedir'], book)))
        except FileNotFoundError: pass
        else:
            self.content = [[
                os.path.splitext(note_file.name)[0],
                str(self._line_count(note_file)),
                datetime.datetime.fromtimestamp(os.stat(note_file).st_atime_ns/1_000_000_000).strftime(config['dateformat']),
                datetime.datetime.fromtimestamp(os.stat(note_file).st_mtime_ns/1_000_000_000).strftime(config['dateformat'])] for note_file in note_files]

        self.empty_content_message = ['No notes detected.', 'Hit n to make one!']
        self.headers = ['NOTE TITLE (F1)  ', 'LINES (F2)  ', 'OPENED (F3)  ', 'MODIFIED (F4)  '] # two spaces so there's room for an arrow when used for sorting
        self.keys = [
                lambda title:title,
                lambda count:int(count),
                lambda datestr:datetime.datetime.strptime(datestr, config['dateformat']),
                lambda datestr:datetime.datetime.strptime(datestr, config['dateformat']) ]
        super().__init__()

    def new(self, title: str):
        raise EditNoteException(self.book, title)

    def rename(self, row: int, new_name: str):
        os.rename(os.path.join(self.config['notedir'], self.book, self.content[row][0] + '.vmnt'), os.path.join(self.config['notedir'], self.book, new_name + '.vmnt'))
        self.content[row][0] = new_name

    def show_delete_dialog(self, row: int):
        self.delete_dialog = DeleteDialog(['Are you sure you want to delete', f'note "{self.content[row][0]}" from book "{self.book}"?', 'This cannot be undone.'])

    def delete(self, row: int):
        pass

    @staticmethod
    def _line_count(file):
        with open(file) as f:
            return len(f.readlines())

    def draw(self, stdscr):
        stdscr.addstr(0,0, f'Book: {self.book}')
        stdscr.clrtoeol()
        super().draw(stdscr)

    def on_enter(self, row: int):
        title = self.content[row][0]
        raise EditNoteException(self.book, title)

    def on_escape(self):
        raise CloseBookException
