#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:10:46 2019

@author: gui
"""
import sys, pygame
import numpy as np
from pygame.locals import *
import pygame.freetype
import random

w = 600
h = 600
scale = 100
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

score = max_score = 0

pygame.init()
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption('2048 - Genérico')

#pygame.freetype.init()
GAME_FONT_BIG = pygame.freetype.SysFont('arial', 80)
GAME_FONT = pygame.freetype.SysFont('arial', 48)
GAME_FONT_SMALL = pygame.freetype.SysFont('arial', 36)
GAME_FONT_SMALLEST = pygame.freetype.SysFont('arial', 24)

grid = np.zeros((4, 4))

def end_game(grid):
    
    GAME_FONT_BIG.render_to(screen, (110, 150), 'Game over', BLUE)
    GAME_FONT_BIG.render_to(screen, (18, 380), 'Continue? (y / n)', BLUE)
    pygame.display.update()
    
    pygame.event.clear()
    event = pygame.event.wait()
    if event.type == KEYDOWN and event.key == K_y:
        global score
        score = 0
        grid = np.zeros((4, 4))
        return grid
    elif event.type == KEYDOWN and event.key == K_n:
        sys.exit()
    else:
        return end_game(grid)


def make_new_rect(grid):
    pos = (np.random.randint(0, 4),
           np.random.randint(0, 4))
    if np.count_nonzero(grid) == 16:
        return end_game(grid)
    elif grid[pos] == 0:
        grid[pos] = np.random.choice([2, 4], p = [.8, .2])
        return grid
    else:
        return make_new_rect(grid)

def move_up(grid):
    cols = grid.shape[1]
    for col in range(cols):
        rows = grid.shape[0]
        for row in range(1, rows):
            for inc in range(row):
                # use inc to roll the lines
                if grid[row - inc, col] == grid[row - inc - 1, col] or grid[row - inc - 1, col] == 0:
                    update_score(grid[row - inc, col], grid[row - inc - 1, col])
                    grid[row - inc - 1, col] += grid[row - inc, col]
                    grid[row - inc, col] = 0
    return make_new_rect(grid)

def move_down(grid):
    cols = grid.shape[1]
    for col in range(cols):
        rows = grid.shape[0]
        for row in range(rows - 2, -1, -1):
            for inc in range(rows - row - 1):
                # use inc to roll the lines
                if grid[row + inc, col] == grid[row + inc + 1, col] or grid[row + inc + 1, col] == 0:
                    update_score(grid[row + inc, col], grid[row + inc + 1, col])
                    grid[row + inc + 1, col] += grid[row + inc, col]
                    grid[row + inc, col] = 0
    return make_new_rect(grid)

def move_right(grid):
    rows = grid.shape[0]
    for row in range(rows):
        cols = grid.shape[1]
        for col in range(cols - 2, -1, -1):
            incs = np.arange(cols - col - 1)
            if len(incs) == 0:
                incs = [0]
            for inc in incs:
                # use inc to roll the lines
                if grid[row, col + inc] == grid[row, col + inc + 1] or grid[row, col + inc + 1] == 0:
                    update_score(grid[row, col + inc], grid[row, col + inc + 1])
                    grid[row, col + inc + 1] += grid[row, col + inc]
                    grid[row, col + inc] = 0
    return make_new_rect(grid)

def move_left(grid):
    rows = grid.shape[0]
    for row in range(rows):
        cols = grid.shape[1]
        for col in range(1, cols):
            for inc in range(col):
                # use inc to roll the lines                
                if grid[row, col - inc] == grid[row, col - inc - 1] or grid[row, col - inc - 1] == 0:
                    update_score(grid[row, col - inc], grid[row, col - inc - 1])
                    grid[row, col - inc - 1] += grid[row, col - inc]
                    grid[row, col - inc] = 0
    return make_new_rect(grid)

def update_score(next, previous):
    global score
    if previous == next:
        score += int(previous + next)
    return None    


clock = pygame.time.Clock()

# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
rect_skin = pygame.Surface ((scale, scale))
rect_skin.fill(WHITE)

GAME_FONT_BIG.render_to(screen, (55, 250), 'Press any key'.format(score), BLUE)
grid = make_new_rect(grid)
pygame.display.update()

pygame.event.clear()
event = pygame.event.wait()

while True:
    max_score = max(max_score, score)
    clock.tick(50)
    screen.fill((0,0,0))
    
    GAME_FONT_SMALLEST.render_to(screen, (380, 20), 'Score: {}'.format(score), WHITE)
    GAME_FONT_SMALLEST.render_to(screen, (380, 50), 'Max Score: {}'.format(max_score), WHITE)
    
    for n_row, row in enumerate(grid):
        for n_col, value in enumerate(row):
            if grid[n_row, n_col] != 0:
                x = n_col * scale + scale
                y = n_row * scale + scale
                screen.blit(rect_skin, (x, y))

                if value < 99:
                    GAME_FONT.render_to(screen, (x + scale // 3, y + scale // 3),
                                        str(int(value)),
                                        (0, 0, 0))
                elif value < 1999:
                    GAME_FONT_SMALL.render_to(screen, (x + scale // 4, y + scale // 2.5),
                                        str(int(value)),
                                        (0, 0, 0))                
                else:
                    GAME_FONT_SMALL.render_to(screen, (x + scale // 6, y + scale // 2.5),
                                        str(int(value)),
                                        (0, 0, 0))                
                    

    #line(Surface, color, start_pos, end_pos, width=1) -> Rect
    for line in range(100, 501, 100):
        pygame.draw.line(screen, (0, 200, 0), (100, line), (500, line), (2))
        pygame.draw.line(screen, (0, 200, 0), (line, 100), (line, 500), (2))
    

    pygame.display.update()
    pygame.event.clear()
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        sys.exit()
    elif event.type == KEYUP and event.key == K_DOWN:
        grid = move_down(grid)
    elif event.type == KEYUP and event.key == K_UP:
        grid = move_up(grid)
    elif event.type == KEYUP and event.key == K_RIGHT:
        grid = move_right(grid)
    elif event.type == KEYUP and event.key == K_LEFT:
        grid = move_left(grid)
