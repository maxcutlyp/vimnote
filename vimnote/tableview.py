import curses
import math
import logging

from typing import List, Callable

class TableView:
    def __init__(self, content: List[List[str]], headers: List[str]):
        self.select_color = curses.COLOR_CYAN
        self.selected = 0
        self.scroll = 0
        self.content = content
        self.headers = headers
        self.sort_by = [3, True] # sort by last edited descending by default
        self.is_searching = False
        self.search_pos = 0
        self.search = None
        self.effective_rows = len(self.content)
        self.pad = curses.newpad(len(self.content)+1, curses.COLS)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)     # header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)      # selection
        try: curses.init_pair(3, 245, -1)                               # greyed out
        except ValueError: curses.init_pair(3, curses.COLOR_WHITE, -1)  # for terminals with only 8 colors
    
    def get_sizes(self):
        sizes = [0] * (len(self.content[0]) - 1)
        for row in self.content + [self.headers]:
            for i,item in enumerate(row[1:]):
                if (size := len(item)) > sizes[i]:
                    sizes[i] = size
        sizes[1] += 1 # dates look too squished next to each other
        return sizes

    def draw_row(self, row_num: int, row: int, sizes: List[int], num_size: int, color_pair):
        so_far = 0
        for item,size in reversed(list(zip(row[1:], sizes))):
            self.pad.addstr(row_num, curses.COLS - size - so_far, item, color_pair)
            so_far += size + 1
        remaining_size = curses.COLS - num_size - so_far - 1
        needs_overflow = len(row[0]) > remaining_size
        size = remaining_size - (1 if needs_overflow else 0)
        self.pad.addstr(row_num, num_size + 1, f'{row[0]:{size}.{size}}{"…" if needs_overflow else ""}', color_pair)

    def draw_row_header(self, stdscr, sizes: List[int], num_size: int):
        so_far = 0
        sort_icon = 'v' if self.sort_by[1] else '^'
        for i,(item,size) in reversed(list(enumerate(zip(self.headers[1:], sizes)))):
            if self.sort_by[0] == i+1:
                color_pair = curses.color_pair(2)
                item = ' ' + item[:-1] + sort_icon + ' '
                offset = 1
            else:
                color_pair = curses.color_pair(1)
                offset = 0
            stdscr.addstr(1, curses.COLS - size - so_far - offset, item, color_pair)
            so_far += size + 1
        size = curses.COLS - num_size - so_far - 3
        is_selected_header = self.sort_by[0] == 0
        stdscr.addstr(1, num_size, f' {self.headers[0]:{size}.{size}} {sort_icon if is_selected_header else ""} ', curses.color_pair(2) if is_selected_header else curses.color_pair(1))

    def draw_search(self, stdscr, num_size: int):
        stdscr.move(2, 0)
        stdscr.clrtoeol()
        if self.search is None:
            stdscr.addstr(2, num_size + 1, 'Search (/)', curses.color_pair(3))
        else:
            if self.is_searching:
                stdscr.addstr(2, 0, ' ' * curses.COLS, curses.color_pair(2))
            stdscr.addstr(2, num_size + 1, f'Search: {self.search}', curses.color_pair(2) if self.is_searching else curses.color_pair(0))
            stdscr.move(2, num_size + 9 + self.search_pos)
        
    def draw(self, stdscr):
        sizes = self.get_sizes()
        num_size = math.floor(math.log10(len(self.content) + 1) + 1)

        # headers
        stdscr.addstr(1, 0, ' '*curses.COLS, curses.color_pair(1))
        self.draw_row_header(stdscr, sizes, num_size)

        # search bar
        self.draw_search(stdscr, num_size)

        # content
        self.pad.clear()
        if not self.is_searching:
            self.pad.addstr(self.selected, 0, ' '*curses.COLS, curses.color_pair(2))
        row_num = 0 # not using enumerate because don't always increment
        for row in self.content:
            if self.search is not None and any(word not in row[0] for word in self.search.split()):
                continue
            color_pair = curses.color_pair(2) if row_num == self.selected and not self.is_searching else curses.color_pair(0)
            self.pad.addstr(row_num, 0, f'{row_num+1:{num_size}}', color_pair)
            self.draw_row(row_num, row, sizes, num_size, color_pair)
            row_num += 1
        self.effective_rows = row_num - 1
        self.pad.refresh(self.scroll, 0, 3, 0, curses.LINES - 1, curses.COLS - 1)

    def switch_sort(self, sort: int):
        logging.log(logging.DEBUG, sort)
        if self.sort_by[0] == sort:
            self.sort_by[1] = not self.sort_by[1]
        else:
            self.sort_by[0] = sort
            self.sort_by[1] = True

    def handle_keypress(self, key: int):
        if not self.is_searching:
            match key:
                case key if key == ord('j'):
                    if self.selected < self.effective_rows:
                        self.selected += 1
                case key if key == ord('k'):
                    if self.selected > 0:
                        self.selected -= 1
                case key if key == ord('/'):
                    self.is_searching = True
                    if self.search is None:
                        self.search = ''
                    curses.curs_set(True)
                case curses.KEY_F1:
                    self.switch_sort(0)
                case curses.KEY_F2:
                    self.switch_sort(1)
                case curses.KEY_F3:
                    self.switch_sort(2)
                case curses.KEY_F4:
                    self.switch_sort(3)
        else:
            char = chr(key)
            if char.isprintable():
                self.search += char
                self.search_pos += 1
                return
            match key:
                case curses.KEY_ENTER | 10:
                    self.is_searching = False
                    curses.curs_set(False)
                    self.selected = 0
                    self.scroll = 0
                case 27: # escape
                    self.is_searching = False
                    self.search_pos = 0
                    curses.curs_set(False)
                    self.search = None
