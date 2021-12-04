from .preview import Preview
import io # for type hinting
from typing import List
import logging

class NotePreview(Preview):
    def __init__(self, pad):
        super().__init__(pad)
        self.content: List[str] = []

    def update(self, row: int, note_file: io.TextIOWrapper):
        super().update(row)
        with note_file:
            self.content = [line[:-1] for line in note_file.readlines()[:self.pad.getmaxyx()[0]]] # remove newlines
            logging.debug((self.content, self.pad.getmaxyx()))

    def draw(self):
        self.pad.clear()
        for row,line in enumerate(self.content):
            self.pad.addstr(row, 0, line)
