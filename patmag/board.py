from .pattern import Pattern

class Board(Pattern):
    def __init__(self, *args, **kwargs):
        super().__init__(height=9, width=9, *args, **kwargs)
        
    @property
    def houses(self):
        houses = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                houses.append(self.read(i, i+2, j, j+2))
        return houses