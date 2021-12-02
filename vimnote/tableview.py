from .exceptions import ExitException
from .textbox import TextBox
import curses
import math
import logging

from typing import List, Callable, Any

class TableView:
    def __init__(self):
        # should be overridden by children, otherwise init to blank
        try: self.content
        except AttributeError: self.content: List[List[str]] = []
        try: self.headers
        except AttributeError: self.headers: List[str] = []
        try: self.keys
        except AttributeError: self.keys: List[str] = []

        self.selected = 0
        self.real_selected = 0 # when searching
        self.scroll = 0
        self.sort_by = [3, True] # sort by last edited descending by default
        self.search_is_visible = False
        self.text_edit_mode = False
        self.effective_rows = len(self.content)
        self.pad = curses.newpad(len(self.content)+1, curses.COLS)
        self.searchbox = TextBox(prompt='Search: ')

        self.noscroll_size = 0.5 # the middle 50% can be navigated without scrolling

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)     # header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)      # selection
        try: curses.init_pair(3, 245, -1)                               # greyed out
        except ValueError: curses.init_pair(3, curses.COLOR_WHITE, -1)  # for terminals with only 8 colors

        self.resort_content()

    # these methods should be overridden by children
    def on_enter(self, row):
        pass 

    def on_escape(self):
        pass

    def new(self):
        pass

    def rename(self, row: int):
        pass

    def delete(self, row: int):
        pass

    def move_row(self, row):
        self.selected = row
        upper_cutoff_size = round((1 - self.noscroll_size)/2 * (curses.LINES-4))
        lower_cutoff_size = round(self.noscroll_size*(curses.LINES-4)) + upper_cutoff_size
        if self.selected > self.scroll + lower_cutoff_size:
            self.scroll = self.selected - lower_cutoff_size
        elif self.selected < self.scroll + upper_cutoff_size:
            self.scroll = self.selected - upper_cutoff_size
        self.scroll = max(0, min(self.scroll, self.effective_rows - (curses.LINES - 4)))
    
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
        if not self.search_is_visible:
            stdscr.addstr(2, num_size + 1, 'Search (/)', curses.color_pair(3))
        else:
            self.searchbox.draw(stdscr, 2, 0, curses.COLS - num_size - 1, curses.color_pair(2) if self.text_edit_mode else curses.color_pair(0), left_offset=num_size+1)
        
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
        if not self.text_edit_mode:
            self.pad.addstr(self.selected, 0, ' '*curses.COLS, curses.color_pair(2))
        row_num = 0 # not using enumerate because don't always increment
        for real_index,row in enumerate(self.content):
            if row_num == self.selected:
                self.real_selected = real_index
            if self.search_is_visible and any(word not in row[0] for word in self.searchbox.text.split()):
                continue
            color_pair = curses.color_pair(2) if row_num == self.selected and not self.text_edit_mode else curses.color_pair(0)
            self.pad.addstr(row_num, 0, f'{row_num+1:{num_size}}', color_pair)
            self.draw_row(row_num, row, sizes, num_size, color_pair)
            row_num += 1
        self.effective_rows = row_num - 1
        self.pad.refresh(self.scroll, 0, 3, 0, curses.LINES - 1, curses.COLS - 1)

    def resort_content(self):
        self.content.sort(key=lambda row: self.keys[self.sort_by[0]](row[self.sort_by[0]]), reverse=self.sort_by[1])

    def switch_sort(self, sort: int):
        if self.sort_by[0] == sort:
            self.sort_by[1] = not self.sort_by[1]
        else:
            self.sort_by[0] = sort
            self.sort_by[1] = sort != 0 # sort titles ascending by default, everything else descending
        self.resort_content()

    def handle_keypress(self, key: int):
        if not self.text_edit_mode:
            match key:
                case key if key == ord('j'):
                    if self.selected < self.effective_rows:
                        self.move_row(self.selected + 1)
                case key if key == ord('k'):
                    if self.selected > 0:
                        self.move_row(self.selected - 1)
                case key if key == ord('G'):
                    self.move_row(self.effective_rows)
                case key if key == ord('g'):
                    self.move_row(0)
                case key if key == ord('/'):
                    self.text_edit_mode = True
                    if not self.search_is_visible:
                        self.searchbox.reset()
                        self.search_is_visible = True
                    curses.curs_set(True)
                case key if key == ord('q'):
                    raise ExitException
                case 4:
                    raise ExitException
                case curses.KEY_F1:
                    self.switch_sort(0)
                case curses.KEY_F2:
                    self.switch_sort(1)
                case curses.KEY_F3:
                    self.switch_sort(2)
                case curses.KEY_F4:
                    self.switch_sort(3)
                case 27: # escape
                    if self.search_is_visible:
                        self.searchbox.reset()
                        self.search_is_visible = False
                    else:
                        self.on_escape()
                case curses.KEY_ENTER | 10:
                    self.on_enter(self.selected)
        else:
            match self.searchbox.handle_keypress(key):
                case 0: # enter
                    self.text_edit_mode = False
                    curses.curs_set(False)
                    self.move_row(0)
                case 1: # escape
                    self.text_edit_mode = False
                    curses.curs_set(False)
                    self.search_is_visible = False
