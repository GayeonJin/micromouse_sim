#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from gobject import *

MAX_ROWS = 16
MAX_COLS = 16

MAZE_XOFFSET = 10
MAZE_YOFFSET = 10

MAZE_WIDTH = 30
MAZE_HEIGHT = 30

WALL_LEFT = 0x01
WALL_BOTTOM = 0x02
WALL_RIGHT = 0x04
WALL_TOP = 0x08
WALL_ALL = 0x0F

WALL_COLOR = COLOR_RED
WALL_WIDTH = 3

class maze_object :
    def __init__(self, rows, cols) :
        self.maze = [] 

        self.rows = rows
        self.cols = cols
        
        for x in range(cols) :
            self.maze.append([])
            for y in range(rows) :
                self.maze[x].append(WALL_ALL)

    def get_size(self) :
        return self.rows, self.cols

    def get_padsize(self) :
        pad_width = 2 * MAZE_XOFFSET + (self.cols + 1) * MAZE_WIDTH
        pad_height = 2 * MAZE_YOFFSET + (self.rows + 1) * MAZE_HEIGHT
        return (pad_width, pad_height) 

    def get_maze_rect(self, x, y) :
        maze_rect = pygame.Rect(MAZE_XOFFSET, MAZE_YOFFSET, MAZE_WIDTH, MAZE_HEIGHT)
        maze_rect.y += self.rows * MAZE_HEIGHT 

        maze_rect.x += x * MAZE_WIDTH
        maze_rect.y -= y * MAZE_HEIGHT
        return maze_rect        

    def get_wall(self, x, y) :
        return self.maze[x][y]

    def draw(self) :
        maze_rect = pygame.Rect(MAZE_XOFFSET, MAZE_YOFFSET, MAZE_WIDTH, MAZE_HEIGHT)

        # maze[0][0] is left and bottom
        maze_rect.y += self.rows * MAZE_HEIGHT 
        for y in range(self.rows) :
            for x in range(self.cols) :
                if self.maze[x][y] & WALL_LEFT :
                    pygame.draw.line(gctrl.gamepad, WALL_COLOR, (maze_rect.left, maze_rect.top), (maze_rect.left, maze_rect.bottom), WALL_WIDTH)
                if self.maze[x][y] & WALL_BOTTOM :
                    pygame.draw.line(gctrl.gamepad, WALL_COLOR, (maze_rect.left, maze_rect.bottom), (maze_rect.right, maze_rect.bottom), WALL_WIDTH)
                if self.maze[x][y] & WALL_RIGHT :
                    pygame.draw.line(gctrl.gamepad, WALL_COLOR, (maze_rect.right, maze_rect.bottom), (maze_rect.right, maze_rect.top), WALL_WIDTH)
                if self.maze[x][y] & WALL_TOP :
                    pygame.draw.line(gctrl.gamepad, WALL_COLOR, (maze_rect.right, maze_rect.top), (maze_rect.left, maze_rect.top), WALL_WIDTH)

                maze_rect.x += MAZE_WIDTH
            maze_rect.y -= MAZE_HEIGHT
            maze_rect.x = MAZE_XOFFSET

    def load(self, filename = 'default_maze.csv') :
        print("load maze : " + filename)

        file = open(filename, 'r')
        rows = csv.reader(file)

        x = 0
        y = 0
        for row in rows :
            for value in row :
                self.maze[x][y] = int(value)
                x += 1
            y += 1
            x = 0

    def save(self, filename = 'default_maze.csv') :
        print("save maze : " + filename)

        with open(filename, 'w') as file:
            #for header in header:
            #    file.write(str(header)+', ')
            #file.write('n')
            for y in range(self.rows):
                for x in range(self.cols-1):
                    file.write(str(self.maze[x][y])+', ')
                file.write(str(self.maze[x+1][y]))
                file.write('\n')

    def edit_wall(self, x, y, wall) :
        if wall != 0 :
            if wall == WALL_LEFT and x > 0 :
                self.maze[x][y] ^= wall 
                self.maze[x-1][y] ^= WALL_RIGHT
            if wall == WALL_RIGHT and x < (self.cols - 1) :
                self.maze[x][y] ^= wall
                self.maze[x+1][y] ^= WALL_LEFT
            if wall == WALL_BOTTOM and y > 0 :
                self.maze[x][y] ^= wall
                self.maze[x][y-1] ^= WALL_TOP
            if wall == WALL_TOP and y < (self.rows - 1) :
                self.maze[x][y] ^= wall
                self.maze[x][y+1] ^= WALL_BOTTOM

        # print(x, y, self.maze[x][y])

if __name__ == '__main__' :
    print('maze object')
