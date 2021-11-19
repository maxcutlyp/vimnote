import curses
import math
import logging

from typing import List

class TableView:
    def __init__(self, content: List[List[str]], headers: List[str]):
        self.select_color = curses.COLOR_CYAN
        self.selected = 0
        self.scroll = 0
        self.content = content
        self.headers = headers
        self.pad = curses.newpad(len(self.content)+1, curses.COLS)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) # header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)  # selection
    
    def get_sizes(self):
        sizes = [0] * (len(self.content[0]) - 1)
        for row in self.content + [self.headers]:
            for i,item in enumerate(row[1:]):
                if (size := len(item)) > sizes[i]:
                    sizes[i] = size
        return sizes

    def draw_row(self, row_num, row, sizes, num_size, pad, color_pair):
        so_far = 0
        for item,size in reversed(list(zip(row[1:], sizes))):
            pad.addstr(row_num, curses.COLS - size - so_far, item, color_pair)
            so_far += size + 1
        remaining_size = curses.COLS - num_size - so_far - 1
        needs_overflow = len(row[0]) > remaining_size
        pad.addstr(row_num, num_size + 1, f'{row[0]:.{remaining_size - (1 if needs_overflow else 0)}}{"…" if needs_overflow else ""}', color_pair)

    def draw(self, stdscr):
        sizes = self.get_sizes()
        num_size = math.floor(math.log10(len(self.content) + 1) + 1)

        # headers
        stdscr.addstr(1, 0, ' '*curses.COLS, curses.color_pair(1))
        self.draw_row(1, self.headers, sizes, num_size, stdscr, curses.color_pair(1))

        # content
        self.pad.addstr(self.selected, 0, ' '*curses.COLS, curses.color_pair(2))
        for i,row in enumerate(self.content):
            color_pair = curses.color_pair(2) if i == self.selected else curses.color_pair(0)
            self.pad.addstr(i, 0, f'{i+1:{num_size}}', color_pair)
            self.draw_row(i, row, sizes, num_size, self.pad, color_pair)
        self.pad.refresh(self.scroll, 0, 2, 0, curses.LINES - 1, curses.COLS - 1)
