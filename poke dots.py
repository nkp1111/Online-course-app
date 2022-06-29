# This program display a game called poke the dots
# It features two dots randomly moving in the display


import pygame
from random import randint
from pygame.time import Clock, get_ticks
from pygame import QUIT, MOUSEBUTTONUP, KEYDOWN, MOUSEBUTTONDOWN
from pygame.mouse import get_pos
from math import sqrt, pow


class Dots:  # class Dots it contains property of the dots.
    def __init__(self, window, color, velocity, radius, centre):
        self.window = window
        self.color = color
        self.velocity = velocity
        self.radius = radius
        self.centre = centre

    # This function draws the dot(circle) inside the display.
    def draw_dot(self):
        pygame.draw.circle(self.window, self.color, (self.centre[0], self.centre[1]), self.radius)

    # This function moves the dots within the display
    def move_dot(self):
        # In this function we add velocity to coordinates of centre of dots
        # centre = [x, y] and velocity = [x, y]
        # velocity in coordinate form changes both x and y coordinates differently.

        size = (self.window.get_width(), self.window.get_height())
        for index in range(2):
            self.centre[index] += self.velocity[index]

            # This step stops the dots from moving outside the given border.
            if (self.centre[index] < self.radius) or (self.centre[index] + self.radius > size[index]):
                self.velocity[index] = -self.velocity[index]

    # This function teleports the dots to some random coordinates
    def randomize_dot(self):
        size = (self.window.get_width(), self.window.get_height())
        for index in range(2):
            self.centre[index] = randint(self.radius, size[index] - self.radius)


# class game represents the whole game structure.
# It carries all the game properties


class Game:
    def __init__(self):
        self._window = create_window('Poke the dots', 500, 400, 'black')
        self._running = True
        self._game_over = False
        self._frame_rate = 45
        self._clock = Clock()
        self._score = 0
        self._small_dot = Dots(self._window, 'red', [2, 1], 25, [25, 25])
        self._big_dot = Dots(self._window, 'blue', [1, 2], 50, [325, 325])

        # This describes all the properties to describe the text
        self._font_family = 'freesansbold.ttf'
        self._font_size = 30
        self._font_position = (0, 0)
        self._font_bgc = None
        self._font_color = 'white'
        self._string = 'None'

    def draw_text(self):
        font = pygame.font.Font(self._font_family, self._font_size)
        text = font.render(self._string, True, self._font_color, self._font_bgc)
        self._window.blit(text, self._font_position)

    # It shows the game score
    # It uses draw_text function to draw the scoreboard
    # It describes the property of the score board
    # like color, position, font, text

    def draw_score(self):
        self._font_size = 30
        self._font_position = (0, 0)
        self._font_bgc = None
        self._font_color = 'white'
        self._string = 'SCORE : ' + str(self._score)
        self.draw_text()

    # This function uses the same method as draw_score.
    # It draws the game over message after the game finishes.
    def draw_game_over(self):
        self._font_size = 30
        self._font_position = (0, self._window.get_height() - self._font_size)
        self._font_color = 'red' or self._small_dot.color
        self._string = 'GAME OVER'
        self._font_bgc = self._big_dot.color
        self.draw_text()

    # game_event describes all the event that happened in the game

    def game_event(self):
        for event in pygame.event.get():
            # It closes the game screen when player click close button at top right corner
            if event.type == QUIT:
                self._running = False

            # It handles the event where player release the mouse button after clicking
            # While the game continues
            elif not self._game_over and event.type == MOUSEBUTTONUP:
                mouse = get_pos()  # It gives mouse position x, y
                self.color_picker()  # 'color_picker' changes the color of the 'small_dot' randomly
                # 'aim_right' function make sure that mouse position is on top of 'big_dot'
                if self.aim_right(self._big_dot, mouse):
                    # It randomly teleports both big_dot and small_dot
                    self._small_dot.randomize_dot()
                    self._big_dot.randomize_dot()

            # It handles events when the key is pressed
            elif not self._game_over and event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    self._big_dot.radius /= 5
                elif event.key == pygame.K_a:
                    self._big_dot.radius *= 5

            # It handles event when mouse clicks down
            # Increases the small_dot velocity
            elif not self._game_over and event.type == MOUSEBUTTONDOWN:
                mouse = get_pos()
                if not self.aim_right(self._big_dot, mouse):
                    for index in range(0, 2):
                        self._small_dot.velocity[index] += 5

        return self._running

    # It moves the dots
    # It changes the frame of the game as per given frame rate
    # It increases the score per second
    def update_game(self):
        self._small_dot.move_dot()
        self._big_dot.move_dot()
        self._clock.tick(self._frame_rate)
        self._score = get_ticks() // 1000

    # play_game while the game continue
    # draw display with given color, small and big dot, scoreboard
    # and continues to update the display screen
    # When the game is over it shows game over

    def play_game(self):
        self._small_dot.randomize_dot()
        self._big_dot.randomize_dot()
        while self._running:
            self._window.fill('black')
            self._small_dot.draw_dot()
            self._big_dot.draw_dot()
            self.draw_score()
            self._game_over = self.is_collision()
            if not self._game_over:
                self.update_game()
            else:
                self.draw_game_over()
            self.game_event()
            pygame.display.update()

    # It detects collision of the two dots and return result
    def is_collision(self):
        distance_btw = 0
        for index in range(0, 2):
            distance_btw += pow(self._small_dot.centre[index] + self._small_dot.velocity[index]
                                - self._big_dot.centre[index] + self._big_dot.velocity[index], 2)
        new_dist = sqrt(distance_btw)
        if new_dist <= (self._small_dot.radius + self._big_dot.radius):
            return True
        else:
            return False

    # It randomly picked a color and returns it
    def color_picker(self):
        self._small_dot.color = [255, 255, 255]
        for index in range(0, 3):
            self._small_dot.color[index] = randint(0, 255)

    # It detects click location of mouse cursor over a particular dot
    def aim_right(self,first_object, second_object):
        distance_btw = 0
        for index in range(0, 2):
            distance_btw += pow(first_object.centre[index] + first_object.velocity[index]
                                - second_object[index], 2)
        new_dist = sqrt(distance_btw)
        if new_dist <= self._big_dot.radius:
            return True
        else:
            return False


def main():
    game = Game()
    game.play_game()


# This function create main window of the game


def create_window(title, width, height, color):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    window.fill(color)
    return window


main()
