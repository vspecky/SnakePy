import pygame
from random import choice

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

WIN_DIMENSIONS = (WIN_WIDTH, WIN_HEIGHT)

DISP = pygame.display.set_mode(WIN_DIMENSIONS)

pygame.display.set_caption('Snake')

CLR_SNAKE = (255, 255, 255)
CLR_FOOD = (255, 50, 50)
CLR_BACK = (25, 25, 25)

CELL_SIZE = 20

ALL_X = list(range(0, WIN_WIDTH + CELL_SIZE, CELL_SIZE))
ALL_Y = list(range(0, WIN_HEIGHT + CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self, x, y, start_dir):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.child = None
        self.dir = start_dir
        self.prev_dir = None

    def draw(self, win):
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.rect(win, CLR_SNAKE, self.rect)

        if self.child != None:
            self.child.draw(win)

    def move(self, next_dir):
        d = next_dir

        if d == 'R':
            self.x = (self.x + CELL_SIZE) % WIN_WIDTH
        elif d == 'L':
            self.x = (self.x - CELL_SIZE) % WIN_WIDTH
        elif d == 'U':
            self.y = (self.y - CELL_SIZE) % WIN_HEIGHT
        elif d == 'D':
            self.y = (self.y + CELL_SIZE) % WIN_HEIGHT

        self.prev_dir = self.dir

        if self.child != None:
            self.child.move(self.dir)

        self.dir = next_dir

    def add(self):
        if self.child != None: return self.child.add()

        d = self.dir
        x = self.x
        y = self.y

        if d == 'R':
            x = (self.x - CELL_SIZE) % WIN_WIDTH
        elif d == 'L':
            x = (self.x + CELL_SIZE) % WIN_WIDTH
        elif d == 'U':
            y = (self.y + CELL_SIZE) % WIN_HEIGHT
        elif d == 'D':
            y = (self.y - CELL_SIZE) % WIN_HEIGHT

        self.child = Snake(x, y, self.prev_dir)

    def remove_occupied(self, vac_x, vac_y):
        if self.x in vac_x:
            vac_x.remove(self.x)

        if self.y in vac_y:
            vac_y.remove(self.y)

        if self.child != None:
            self.child.remove_occupied(vac_x, vac_y)
        

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def draw(self, win):
        self.rect.topleft = (self.x, self.y)
        pygame.draw.rect(win, CLR_FOOD, self.rect)

    def change_location(self, vac_x, vac_y):
        self.x = choice(vac_x)
        self.y = choice(vac_y)

def change_food_location(food, snake):
    vac_x = [x for x in ALL_X]
    vac_y = [y for y in ALL_Y]

    vac_x.remove(800)
    vac_y.remove(600)

    snake.remove_occupied(vac_x, vac_y)

    food.change_location(vac_x, vac_y)

def check_snake_eat_self(snake):
    head = snake
    cell = head.child

    while cell != None:
        if head.rect.colliderect(cell.rect):
            return True
        cell = cell.child

    return False

def snake_eat_phood(snake, food):
    if snake.rect.colliderect(food.rect):
        snake.add()
        change_food_location(food, snake)
        return True

    return False

def draw_game(win, snake, food):
    win.fill(CLR_BACK)

    food.draw(win)
    snake.draw(win)

    pygame.display.update()

def quit_game():
    pygame.quit()
    quit()

def main_loop():

    gen_dir = 'R'
    clock = pygame.time.Clock()
    snek = Snake(20, 20, gen_dir)
    phood = Food(80, 80)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and gen_dir != 'D':
                    gen_dir = 'U'
                elif event.key == pygame.K_DOWN and gen_dir != 'U':
                    gen_dir = 'D'
                elif event.key == pygame.K_LEFT and gen_dir != 'R':
                    gen_dir = 'L'
                elif event.key == pygame.K_RIGHT and gen_dir != 'L':
                    gen_dir = 'R'

        snek.move(gen_dir)

        if check_snake_eat_self(snek):
            quit_game()

        snake_eat_phood(snek, phood)

        draw_game(DISP, snek, phood)

        pygame.time.delay(100)

main_loop()