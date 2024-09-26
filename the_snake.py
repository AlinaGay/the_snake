from random import choice
from typing import Optional

import pygame as pg

# Constants for the field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MID_OF_SCREEN = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Direction of movement:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTION_LIST = [UP, DOWN, LEFT, RIGHT]

# Background color: black
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Color of the cell border
BORDER_COLOR = (93, 216, 228)

# Color of the apple
APPLE_COLOR = (255, 92, 126)

# Color of the snake
SNAKE_COLOR = (255, 190, 103)

# Snake speed:
SPEED = 10

# Settings for the playground window:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Head name of the playground window:
pg.display.set_caption('Змейка')

# Time settings:
clock = pg.time.Clock()


class GameObject:
    """Class that describes the playing object."""

    def __init__(self) -> None:
        self.position = MID_OF_SCREEN
        self.body_color: Optional[tuple[int, int, int]] = None

    def draw(self, position, body_color=None, border_color=None):
        """Public method that draws the playing object."""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Snake(GameObject):
    """Class that describes the snake."""

    def __init__(self) -> None:
        super().__init__()
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.filled_positions = self.positions

    def update_direction(self):
        """Public method that updates the direction"""
        """after pressing the button."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Public method for moving the snake."""
        current_head_x, current_head_y = self.get_head_position()
        new_head_x = (
            (current_head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH)
        new_head_y = (
            (current_head_y + self.direction[1] * GRID_SIZE) % SCREEN_WIDTH)
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def draw(self):
        """Public method that draws the snake."""
        for position in self.positions[:-1]:
            super().draw(position, SNAKE_COLOR, BORDER_COLOR)

        # Drawing a head of the snake
        super().draw(self.positions[0], SNAKE_COLOR, BORDER_COLOR)

        # Removing the last segment
        if self.last:
            super().draw(self.last, BOARD_BACKGROUND_COLOR,
                         BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Public method that returns the head position."""
        return self.positions[0]

    def get_longer(self):
        """Public method that adds segments to the snake."""
        self.positions.append(self.last)
        self.last = None

    def reset(self):
        """Public method that returns the snake to an initial state."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        self.direction = choice(DIRECTION_LIST)


class Apple(GameObject):
    """Class that describes the apple."""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Public method that draws the apple."""
        super().draw(self.position, APPLE_COLOR, BORDER_COLOR)

    def randomize_position(self):
        """Public method that sets the apple position"""
        """randomly on the playing field."""
        apple_position_x = choice(range(0, 640, 20))
        apple_position_y = choice(range(0, 480, 20))
        while (apple_position_x, apple_position_y) in Snake().positions:
            apple_position_x = choice(range(0, 640, 20))
            apple_position_y = choice(range(0, 480, 20))
        else:
            self.position = (apple_position_x, apple_position_y)
        return self.position


def handle_keys(game_object):
    """Public function for processing of user activity"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Public function that describes the whole game"""
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.get_longer()
            apple.randomize_position()

        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
