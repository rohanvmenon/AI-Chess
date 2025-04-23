class Move:

    def __init__(self, initial, final, piece=None):
        # initial and final are squares
        self.initial = initial
        self.final = final
        self.piece = piece  # Add this attribute to store the piece being moved

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final