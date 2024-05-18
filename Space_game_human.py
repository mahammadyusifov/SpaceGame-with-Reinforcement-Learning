import pygame
import random
from collections import namedtuple
import torch

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# CONSTANTS OF THE GAME
LEFT = 1
MIDDLE = 2
RIGHT = 3
POINT_SIZE = 50

WHITE = (255, 255, 255)
RED = (200,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,207,64)

SPEED = 7

SHIP = pygame.image.load('space_ship_pixel.png')
ENEMY1 = pygame.image.load('enemy1.png')
ENEMY2 = pygame.image.load('enemy2.png')
COIN = pygame.image.load('coin.png')

DEFAULT_IMAGE_POSITION = (100,100)
DEFAULT_IMAGE_SIZE = (POINT_SIZE,POINT_SIZE)

SHIP = pygame.transform.scale(SHIP, DEFAULT_IMAGE_SIZE)
ENEMY1 = pygame.transform.scale(ENEMY1, DEFAULT_IMAGE_SIZE)
ENEMY2 = pygame.transform.scale(ENEMY2, DEFAULT_IMAGE_SIZE)
COIN = pygame.transform.scale(COIN, DEFAULT_IMAGE_SIZE)

# What a Point is
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
class Space_Game:

    def __init__(self, w = 3*POINT_SIZE, h=12*POINT_SIZE):
        # Size of screen and setting up screen / time 
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SpaceShip')
        self.clock = pygame.time.Clock()

        # initial game state
        self.position = Point(MIDDLE*POINT_SIZE, (-1+self.h//POINT_SIZE)*POINT_SIZE)

        self.enemies = []
        self.rewards = []
        self.score = 0
        self._place_enemy()
        self._place_reward()

    def _place_enemy(self):
        x =random.choice([LEFT, MIDDLE, RIGHT])*POINT_SIZE
        y = 0
        enemy = Point(x,y)
        self.enemies.append(enemy)
        
    def _place_reward(self):
        x = random.choice([LEFT, MIDDLE, RIGHT])*POINT_SIZE
        y = 0
        reward = Point(x,y)
        self.rewards.append(reward)
    
    def _enemy_move(self):
        for pt in self.enemies:
            pt.y = pt.y + POINT_SIZE
    def _reward_move(self):
        for pt in self.rewards:
            pt.y = pt.y + POINT_SIZE

    def _play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.position.x != LEFT:
                        self.position.x = int(self.position.x)- POINT_SIZE
                if event.key == pygame.K_RIGHT and int(self.position.x) != RIGHT:
                    self.position.x = self.position.x + POINT_SIZE

            
        # 2 stuff moves
        self._ship_move(self.position)
        self._enemy_move()
        self._reward_move()
        
        if random.choice(['enemy', 'reward', 'pass1', 'pass2', 'pass3', 'pass4', 'pass5']) == 'enemy':
            self._place_enemy()
        elif random.choice(['enemy', 'reward', 'pass1', 'pass2', 'pass3']) == 'reward':
            self._place_reward()
        # 3 check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        # 4. get reward or just move
        for pt in self.rewards:
            if (self.position.x, self.position.y) == (pt.x, pt.y):
                self.rewards.remove(pt)
                self.score += 1
                break
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return game_over, self.score
        
    def _is_collision(self):
        # hits enemy
        # enemy hits boundary
        if self.position.x < 0 or self.position.x == self.w:
            return True
        # hits enemy
        for pt in self.enemies:
            if self.position.x == pt.x and self.position.y == pt.y: # - POINT_SIZE 
                return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)

        self.display.blit(SHIP, (self.position.x, self.position.y))

        for pt in self.enemies:
            self.display.blit(ENEMY1, (pt.x, pt.y))
        for pt in self.rewards:
            self.display.blit(COIN, (pt.x, pt.y))
        text = font.render('Score:' + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _ship_move(self, position):
        self.position = position
        
if __name__ == '__main__':
    game = Space_Game()
    # game loop
    while True:
        game_over, score = game._play_step()

        if game_over == True:
            break
    print('Final Score', score)

    pygame.quit()