from random import choice, randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Class that describes the playing object."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color: Optional[tuple[int, int, int]] = None

    def draw(self):
        """Public method that draws the playing object."""
        pass


class Snake(GameObject):
    """Class that describes the snake."""

    def __init__(self):
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = len(self.positions)
        self.last = self.positions[-1]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Public method that updates the direction"""
        """after pressing the button."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Public method for moving the snake."""
        if self.direction:
            for seg in self.positions:
                seg_list = list(seg)
                seg_list[0] = seg_list[0] + self.direction[0]
                seg_list[1] = seg_list[1] + self.direction[1]
                seg = tuple(seg_list)
        return self.positions

    def draw(self):
        """Public method that draws the snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Drawing a head of the snake
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Removing the last segment
        """ if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect) """

    def get_head_position(self):
        """Public method that returns the head position."""
        return self.positions[0]


class Apple(GameObject):
    """Class that describes the apple."""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Public method that draws the apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Public method that sets the apple position"""
        """randomly on the playing field."""
        x = choice(range(0, 640, 20))
        y = choice(range(0, 480, 20))
        self.position = (x, y)
        return self.position


def handle_keys(game_object):
    """Public function for processing of user activity"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Public function that describes the whole game"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        pygame.display.update()

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()
