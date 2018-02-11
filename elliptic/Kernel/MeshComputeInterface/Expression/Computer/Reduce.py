from .Computer import Computer


class Reduce(Computer):
    
    def __init__(self):
        super().__init__()


class Sum(Reduce):

    def __init__(self):
        super().__init__()

        self.name = f"Reduce\nsum"