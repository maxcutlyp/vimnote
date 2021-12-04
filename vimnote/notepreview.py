from .preview import Preview
import io # for type hinting
from typing import List
import logging
import textwrap

class NotePreview(Preview):
    def __init__(self, pad):
        super().__init__(pad)
        self.content: List[str] = []

    def update(self, row: int, note_file: io.TextIOWrapper):
        super().update(row)
        with note_file:
            # split the file by newlines and by text wrap
            self.content = [line for rawline in note_file.readlines()[:self.pad.getmaxyx()[0] - 2]
                    for line in textwrap.fill(rawline[:-1], self.pad.getmaxyx()[1] - 2).split('\n')]

    def draw(self):
        self.pad.clear()
        width = self.pad.getmaxyx()[1]
        self.pad.addstr(0, 0, f'{"─" * width}')
        for row,line in enumerate(self.content):
            self.pad.addstr(row + 1, 1, line)
