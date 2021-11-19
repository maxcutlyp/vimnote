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
        self.sort_by = [3, True] # sort by last edited descending by default
        self.pad = curses.newpad(len(self.content)+1, curses.COLS)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) # header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)  # selection
    
    def get_sizes(self):
        sizes = [0] * (len(self.content[0]) - 1)
        for row in self.content + [self.headers]:
            for i,item in enumerate(row[1:]):
                if (size := len(item)) > sizes[i]:
                    sizes[i] = size
        sizes[1] += 1 # dates look too squished next to each other
        return sizes

    def draw_row(self, row_num, row, sizes, num_size, pad, color_pair, is_header):
        so_far = 0
        for i,(item,size) in reversed(list(enumerate(zip(row[1:], sizes)))):
            logging.log(logging.DEBUG, i)
            mod_color_pair = color_pair
            if is_header and self.sort_by[0] == i+1:
                mod_color_pair = curses.color_pair(2)
                item = f'{item[:-1]:{size-1}}{"v" if self.sort_by[1] else "^"} '
            pad.addstr(row_num, curses.COLS - size - so_far, item, mod_color_pair)
            so_far += size + 1
        remaining_size = curses.COLS - num_size - so_far - 1
        needs_overflow = len(row[0]) > remaining_size
        is_selected_header = is_header and self.sort_by[0] == 0
        if is_selected_header:
            sort_icon = 'v' if self.sort_by[1] else '^'
            color_pair = curses.color_pair(2)
        else:
            sort_icon = ''
        size = remaining_size - (1 if needs_overflow else 0) - (1 if is_selected_header else 0)
        pad.addstr(row_num, num_size + 1, f'{row[0]:{size}.{size}}{"…" if needs_overflow else ""}{sort_icon} ', color_pair)

    def draw(self, stdscr):
        sizes = self.get_sizes()
        num_size = math.floor(math.log10(len(self.content) + 1) + 1)

        # headers
        stdscr.addstr(1, 0, ' '*curses.COLS, curses.color_pair(1))
        self.draw_row(1, self.headers, sizes, num_size, stdscr, curses.color_pair(1), True)

        # content
        self.pad.clear()
        self.pad.addstr(self.selected, 0, ' '*curses.COLS, curses.color_pair(2))
        for i,row in enumerate(self.content):
            color_pair = curses.color_pair(2) if i == self.selected else curses.color_pair(0)
            self.pad.addstr(i, 0, f'{i+1:{num_size}}', color_pair)
            self.draw_row(i, row, sizes, num_size, self.pad, color_pair, False)
        self.pad.refresh(self.scroll, 0, 2, 0, curses.LINES - 1, curses.COLS - 1)

    def handle_keypress(self, key):
        match key:
            case key if key == ord('j'):
                if self.selected < len(self.content):
                    self.selected += 1
            case key if key == ord('k'):
                if self.selected > 0:
                    self.selected -= 1
