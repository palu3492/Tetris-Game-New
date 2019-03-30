# Tetris piece class
import random
import pygame
from Square import Square

class Piece:

    # Pieces with rotations
    pieces = [
        ["110,011",
         "01,11,10",
         "110,011",
         "01,11,10"],
        ["1,1,1,1",
         "1111"],
        ["11,11"],
        ["011,110",
         "10,11,01"],
        ["10,10,11",
         "111,100",
         "11,01,01",
         "001,111"],
        ["01,01,11",
         "100,111",
         "11,10,10",
         "111,001"],
        ["111,010",
         "01,11,01",
         "010,111",
         "10,11,10"]
    ]

    def __init__(self, pygame_screen):
        # Index of piece from pieces class variable
        self.piece_number = 0
        # Index of rotation of piece from pieces class variable
        self.piece_rotation = 0
        # Number corresponding to color of square image in ./squares
        self.color = 1
        # Array of rotations from pieces class variable
        self.piece_array = []

        self.piece_string = ""
        self.squares = []
        self.pygame_screen = pygame_screen
        self.setup()
        self.row = -len(self.piece_string.split(","))
        self.column = 4

    def setup(self):
        self.piece_number = random.randint(0, 6)
        self.color = self.piece_number+1
        self.piece_array = Piece.pieces[self.piece_number]
        self.piece_string = self.piece_array[self.piece_rotation]

        col_counter = 0
        row_counter = -len(self.piece_string.split(","))
        for row in self.piece_string.split(","): #111
            for col in row:
                if col == "1":
                    self.squares.append(Square(self.pygame_screen, self.color, col_counter+4, row_counter))
                col_counter += 1
            col_counter = 0
            row_counter += 1

    def rotate(self, new_squares):
        self.piece_rotation = self.get_next_rotation()
        self.squares = new_squares

    def get_next_rotation(self):
        new_rotation = self.piece_rotation + 1
        if new_rotation >= len(self.piece_array):
            new_rotation = 0
        return new_rotation

    def get_rotate_squares(self):
        new_rotation = self.get_next_rotation()
        new_piece_string = self.piece_array[new_rotation]

        row_counter = self.row
        col_counter = self.column
        new_squares = []
        for row in new_piece_string.split(","):
            for col in row:
                if col == "1":
                    new_squares.append(Square(self.pygame_screen, self.color, col_counter, row_counter))
                col_counter += 1
            col_counter = self.column
            row_counter += 1
        return new_squares

    def move_down(self):
        for square in self.squares:
            square.move_down()
        self.row += 1

    def move_sideways(self, direction):
        for square in self.squares:
            square.move_sideways(direction)
        if direction == 'right':
            self.column += 1
        else:
            self.column -= 1

    def blit(self):
        for square in self.squares:
            square.blit()

    def get_squares(self):
        return self.squares
