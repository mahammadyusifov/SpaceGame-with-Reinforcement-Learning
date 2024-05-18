import pygame
import random
import numpy as np 

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

LEFT = 0
MIDDLE_LEFT = 1
MIDDLE_RIGHT = 2
RIGHT = 3

POINT_SIZE = 50

WHITE = (255, 255, 255)
RED = (200,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,207,64)

SHIP = pygame.image.load('space_ship_pixel.png')
ENEMY1 = pygame.image.load('enemy1.png')
ENEMY2 = pygame.image.load('enemy2.png')
COIN = pygame.image.load('coin.png')

DEFAULT_IMAGE_SIZE = (POINT_SIZE,POINT_SIZE)

SHIP = pygame.transform.scale(SHIP, DEFAULT_IMAGE_SIZE)
ENEMY1 = pygame.transform.scale(ENEMY1, DEFAULT_IMAGE_SIZE)
ENEMY2 = pygame.transform.scale(ENEMY2, DEFAULT_IMAGE_SIZE)
COIN = pygame.transform.scale(COIN, DEFAULT_IMAGE_SIZE)

SPEED = 10

class SpaceGame:

    def __init__(self, w = 10*POINT_SIZE, h = 10*POINT_SIZE):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SpaceGame')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # resets game to beginning
        x = random.choice([LEFT, MIDDLE_LEFT, MIDDLE_RIGHT, RIGHT]) * POINT_SIZE
        y = self.h - POINT_SIZE
        self.position = np.array([x, y], dtype=float).reshape(-1,2)

        self.score = 0
        # self.ammo_left = 0
        self.enemies = np.empty((0,2))
        self.coins = np.empty((0,2))
        self._place_coin()
        self._place_enemy()
        # self.ammoes = np.array([])

    def _place_coin(self):
        x = random.choice([LEFT, MIDDLE_LEFT, MIDDLE_RIGHT, RIGHT]) * POINT_SIZE
        y = 0
        coin = np.array([x, y])
        self.coins = np.append(self.coins, coin)
        self.coins = self.coins.reshape(-1, 2)

    def _place_enemy(self):
        x = random.choice([LEFT, MIDDLE_LEFT, MIDDLE_RIGHT, RIGHT]) * POINT_SIZE
        y = 0
        enemy = np.array([x, y])
        self.enemies = np.append(self.enemies, enemy)
        self.enemies = self.enemies.reshape(-1, 2)

    def _move_stuff(self):
        self.enemies[:, 1] += POINT_SIZE
        self.coins[:, 1] += POINT_SIZE
        self.enemies = self.enemies[self.enemies[:, 1] < self.h]
        self.coins = self.coins[self.coins[:, 1] < self.h]

    def _there_is_collision(self):
        if np.any(np.all(self.enemies == self.position, axis=1)):
            return True
        return False
    
    def _move_ship(self, action):
        if np.array_equal(action, np.array([1, 0, 0])) and self.position[0,0] != 0:
            self.position[0, 0] -= POINT_SIZE
        elif np.array_equal(action, np.array([0, 1, 0])) and  self.position[0,0] != 3*POINT_SIZE:
            self.position[0,0] += POINT_SIZE

    def _update_ui(self):

        self.display.fill(BLACK)
        self.display.blit(SHIP, tuple(self.position))
        for pt in self.enemies:
            self.display.blit(ENEMY1, tuple(pt))
        for pt in self.coins:
            self.display.blit(COIN, tuple(pt))
        
        text = font.render('Score:' + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _play_step(self, action):
        # 1. check if quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # 2. do the action
        self._move_stuff()
        self._move_ship(action)
        i  = random.choice([-1, 0 , 2])
        if i == -1:
            self._place_enemy()
        elif i == 1:
            self._place_coin()
        # 3. check if game over
        reward = 0
        game_over = False
        if self._there_is_collision(
            
        ) :
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. check if got coins
        if np.any(np.all(self.coins == self.position, axis=1)):
            self.score += 1
            reward += 20
            self._place_coin()
        # 5. update ui and time
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score