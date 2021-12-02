import curses

class TextBox:
    def __init__(self, prompt: str = None):
        self.text = ''
        self.cursor_pos = 0

    def draw(self, win, y: int, x: int, length: int, color_pair):
        pass

    def handle_keypress(key: int):
        pass
