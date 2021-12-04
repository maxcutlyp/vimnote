class Preview:
    def __init__(self, pad):
        self.pad = pad
        self.internal_row = 0 # so we know whether to update or not

    def update(self, row: int, *args):
        self.internal_row = row

    def draw(self):
        pass
