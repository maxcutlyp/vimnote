import curses
from .exceptions import ExitException

class TextBox:
    def __init__(self, prompt: str = ''):
        self.prompt = prompt
        self.reset()

    def reset(self):
        self.text = ''
        self.cursor_pos = 0

    def draw(self, win, y: int, x: int, size: int, color_pair, left_offset: int = 0):
        # TODO: implement scrolling similarly to how it's implemented in tableview
        win.addstr(y, x, f'{" " * left_offset}{self.prompt}{self.text}{" " * (size - len(self.text) - len(self.prompt))}', color_pair)
        win.move(y, x + left_offset + len(self.prompt) + self.cursor_pos)

    def handle_keypress(self, key: int) -> int:
        match key:
            case curses.KEY_BACKSPACE | 127 | 8:
                self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                self.cursor_pos = max(self.cursor_pos - 1, 0)
            case curses.KEY_DC:
                self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                self.cursor_pos = min(self.cursor_pos, len(self.text))
            case curses.KEY_LEFT:
                self.cursor_pos = max(self.cursor_pos - 1, 0)
            case curses.KEY_RIGHT:
                self.cursor_pos = min(self.cursor_pos + 1, len(self.text))
            case curses.KEY_UP:
                self.cursor_pos = 0
            case curses.KEY_DOWN:
                self.cursor_pos = len(self.text)
            case curses.KEY_ENTER | 10:
                return 0
            case 27: # escape
                self.cursor_pos = 0
                self.text = ''
                return 1
            case 4:
                raise ExitException
            case _:
                char = chr(key)
                if char.isprintable():
                    self.text = self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
        return -1
