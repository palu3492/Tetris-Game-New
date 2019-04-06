# Alex Palumbo

import pygame
import random
from Piece import Piece
from Square import Square
from Particle import Particle

class Tetris:

    def __init__(self):
        self.pygame_screen = None
        self.clock = None
        self.font = None
        self.piece = None
        self.squares = []
        self.particles = []
        self.outer_squares = []
        self.drops_per_second = 6
        self.frames_per_second = 30
        self.score = 0
        self.lines = 0
        self.high_score = int(open("files/highscore.txt", "r").read())
        self.background = pygame.image.load('files/images/background4.jpg')
        self.game_running = True
        self.setup()

    def setup(self):
        pygame.init()
        pygame.font.init()
        self.pygame_screen = pygame.display.set_mode((582,785))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('files/fonts/arial.ttf', 45)

    def splash_screens(self):
        self.splash_screen()
        self.start_screen()

    def start_game(self):
        self.game_loop()

    def splash_screen(self):
        frame_counter = 0
        self.pygame_screen.blit(pygame.image.load('files/images/splash.jpg'), (0, 0))
        while frame_counter < 30 and self.game_running:
            frame_counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
            pygame.display.update()
            self.clock.tick(self.frames_per_second)

    def start_screen(self):
        space_pressed = False
        while not space_pressed and self.game_running:
            self.pygame_screen.blit(pygame.image.load('files/images/background5.jpg'), (0, 0))
            self.pygame_screen.blit(pygame.image.load('files/images/startButton.png'), (231, 360))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                elif event.type == pygame.QUIT:
                    self.game_running = False
            pygame.display.update()
            self.clock.tick(self.frames_per_second)

    def game_loop(self):
        frame_counter = 1
        self.create_floor()
        self.create_walls()
        self.new_piece()
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.move_piece_sideways('left')
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_piece_sideways('right')
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.rotate_piece()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.move_piece_down()
                    if event.key == pygame.K_SPACE:
                        self.drop_piece()

            if frame_counter % (self.frames_per_second/self.drops_per_second) == 0:
                self.move_piece_down()

            frame_counter += 1

            self.blit_everything()
            pygame.display.update()
            self.clock.tick(self.frames_per_second)

    def create_floor(self):
        for col in range(10):
            self.outer_squares.append(Square(None, 8, col, 18))

    def create_walls(self):
        for row in range(-1, 18):
            self.outer_squares.append(Square(None, 8, -1, row))
        for row in range(-1, 18):
            self.outer_squares.append(Square(None, 8, 10, row))

    def new_piece(self):
        self.piece = Piece(self.pygame_screen)

    def move_piece_down(self):
        if self.can_piece_move_down():
            self.piece.move_down()
            return True
        else:
            self.piece_collide()
            return False

    def move_piece_sideways(self, direction):
        if self.can_piece_move_sideways(direction):
            self.piece.move_sideways(direction)

    def can_piece_move_down(self):
        for piece_square in self.piece.get_squares():
            for board_square in self.squares + self.outer_squares:
                if piece_square.get_column() == board_square.get_column() and piece_square.get_row() + 1 == board_square.get_row():
                    return False
        return True

    def can_piece_move_sideways(self, direction):
        if direction == 'right':
            direction_number = 1
        else:
            direction_number = -1
        for piece_square in self.piece.get_squares():
            for board_square in self.squares + self.outer_squares:
                if piece_square.get_column() + direction_number == board_square.get_column() and piece_square.get_row() == board_square.get_row():
                    return False
        return True

    def rotate_piece(self):
        new_squares = self.can_rotate_piece()
        if new_squares is not False:
            self.piece.rotate(new_squares)

    def can_rotate_piece(self):
        new_squares = self.piece.get_rotate_squares()
        for piece_square in new_squares:
            for board_square in self.squares + self.outer_squares:
                if (piece_square.get_column(), piece_square.get_row()) == (board_square.get_column(), board_square.get_row()):
                    return False
        return new_squares

    def piece_collide(self):
        if self.did_lose():
            self.ask_play_again()
        else:
            self.squares += self.piece.get_squares()
            self.check_line_win()
            self.new_piece()

    def blit_everything(self):
        self.pygame_screen.blit(self.background, (0, 0))
        self.piece.blit()
        for square in self.squares:
            square.blit()
        self.blit_scores()
        self.blit_particles()

    def blit_particles(self):
        index = 0
        for i in range(len(self.particles)):
            particle = self.particles[index]
            particle.blit()
            if not particle.blit():
                del self.particles[index]
            else:
                index += 1

    def check_line_win(self):
        row_dictionary = {}
        for square in self.squares:
            square_row = square.get_row()
            if square_row in row_dictionary:
                row_dictionary[square_row] += 1
            else:
                row_dictionary[square_row] = 1
        win_count = 0
        for row in sorted(row_dictionary):
            # row_dictionary[row] = 10 #always win
            if row_dictionary[row] == 10:
                win_count += 1
                self.add_particles(row)
                self.delete_row(row)
                self.drop_rows_down(row)
        if win_count > 0:
            self.lines += win_count
            self.add_to_score(win_count)

    def add_particles(self, line):
        for square in self.squares:
            if square.get_row() == line:
                for row in range(2):
                    for col in range(15):
                        self.particles.append(Particle(self.pygame_screen, col, row, line, 5))

    def delete_row(self, row):
        index = 0
        for i in range(len(self.squares)):
            square = self.squares[index]
            if square.get_row() == row:
                del self.squares[index]
            else:
                index += 1

    def drop_rows_down(self, start):
        for square in self.squares:
            if square.get_row() < start:
                square.move_down()

    def drop_piece(self):
        while self.move_piece_down():
            pass

    def add_to_score(self, win_count):
        new_score = 0
        for i in range(win_count):
            new_score += ((i+1) * 10)
        self.score += new_score
        if self.score > self.high_score:
            self.high_score = self.score
            open("files/highscore.txt", "w").write(str(self.high_score))


    def blit_scores(self):
        block = self.font.render(str(self.lines), True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (510, 250)
        self.pygame_screen.blit(block, rect)

        block = self.font.render(str(self.score), True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (510, 350)
        self.pygame_screen.blit(block, rect)

        block = self.font.render(str(self.high_score), True, (0, 0, 0))
        rect = block.get_rect()
        rect.center = (510, 465)
        self.pygame_screen.blit(block, rect)

    def did_lose(self):
        for square in self.piece.get_squares():
            if square.get_row()< 0:
                return True
        return False

    def ask_play_again(self):
        space_pressed = False
        while not space_pressed and self.game_running:
            self.pygame_screen.blit(pygame.image.load('files/images/playAgainButton.png'), (231, 360))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                        self.reset_game()
                elif event.type == pygame.QUIT:
                    self.game_running = False
            pygame.display.update()
            self.clock.tick(self.frames_per_second)

    def reset_game(self):
        self.piece = None
        self.squares = []
        self.score = 0
        self.lines = 0
        self.new_piece()


tetris = Tetris()
tetris.splash_screens()
tetris.start_game()
