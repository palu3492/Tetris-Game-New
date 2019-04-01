# Tetris particle class
import pygame
import random

class Particle:

    def __init__(self, pygame_screen, x, y, line, color):
        self.pygame_screen = pygame_screen
        self.vertical_amount = random.randrange(-10,10)
        self.horizontal_amount = random.randrange(-10,10)
        self.x = 146 + 6 + (x * 19)
        self.y = (line * 29) + 193 + 5 + (y * 15)
        self.image = pygame.image.load("files/squares/particle%d.jpg" % random.randint(1,7))
        self.alpha_amount = 225

        #146, 437

    def blit(self):
        self.alpha_amount -= 25
        self.image.set_alpha(self.alpha_amount)
        self.x += self.horizontal_amount
        self.y += self.vertical_amount
        self.pygame_screen.blit(self.image, (self.x, self.y))
        if self.alpha_amount < 0:
            return False
        return True


