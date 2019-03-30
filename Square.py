# Tetris square class
import pygame
# import numpy

class Square:

    def __init__(self, pygame_screen, color, column, row):
        self.pygame_screen = pygame_screen
        self.color = color
        # self.grid_coordinates = (col, row)
        self.row = row
        self.column = column
        self.screen_coordinates = (0, 0)
        self.image = pygame.image.load("files/squares/color%d.jpg" % color)

    def blit(self):
        if self.row >= 0:
            self.convert_grid_to_screen()
            self.pygame_screen.blit(self.image, self.screen_coordinates)

    def convert_grid_to_screen(self):
        self.screen_coordinates = ((self.column*29)+147, (self.row*29)+193)

    def move_down(self):
        # self.grid_coordinates = tuple(numpy.add(self.grid_coordinates, (0, 1)))
        self.row += 1

    def move_sideways(self, direction):
        if direction == 'right':
            # self.grid_coordinates = tuple(numpy.add(self.grid_coordinates, (1, 0)))
            self.column += 1
        else:
            # self.grid_coordinates = tuple(numpy.subtract(self.grid_coordinates, (1, 0)))
            self.column -= 1

    # def get_grid_coordinates(self):
    #     return self.grid_coordinates

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column


