import curses
import math
import logging

from typing import List

class TableView:
    def __init__(self, content: List[List[str]]):
        self.select_color = curses.COLOR_CYAN
        self.selected = 0
        self.scroll = 0
        self.content = content
        self.pad = curses.newpad(len(self.content)+1, curses.COLS)
    
    def get_sizes(self):
        sizes = [0] * (len(self.content[0]) - 1)
        for row in self.content:
            for i,item in enumerate(row[1:]):
                if (size := len(item)) > sizes[i]:
                    sizes[i] = size
        return sizes

    def draw(self, stdscr):
        sizes = self.get_sizes()
        num_size = math.floor(math.log10(len(self.content) + 1) + 1)

        # content
        for i,row in enumerate(self.content):
            self.pad.addstr(i, 0, str(i + 1))
            so_far = 0
            for item,size in reversed(list(zip(row[1:], sizes))):
                self.pad.addstr(i, curses.COLS - size - so_far, item)
                so_far += size + 1
            remaining_size = curses.COLS - num_size - so_far - 2
            needs_overflow = len(row[0]) > remaining_size
            self.pad.addstr(i, num_size + 2, f'{row[0]:.{remaining_size - (1 if needs_overflow else 0)}}{"…" if needs_overflow else ""}')
        self.pad.refresh(self.scroll, 0, 2, 0, curses.LINES - 1, curses.COLS - 1)
