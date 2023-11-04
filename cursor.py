#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from gobject import *
from maze import *

CURSOR_MOVE_LEFT = 1
CURSOR_MOVE_DOWN = 2
CURSOR_MOVE_RIGHT = 4
CURSOR_MOVE_UP = 8

class cursor_object :
    def __init__(self, maze) :
        self.x = 0
        self.y = 0
        self.maze = maze

        self.rows, self.cols = self.maze.get_size()

    def get_cur_pos(self) :
        return [self.x, self.y]

    def set_pos(self, x, y) :
        self.x = x
        self.y = y

    def move(self, direction) :
        if direction == CURSOR_MOVE_UP:
            self.y += 1
            if self.y >= self.rows :
                self.y = self.rows - 1
        elif direction == CURSOR_MOVE_DOWN :
            self.y -= 1
            if self.y < 0 :
                self.y = 0
        elif direction == CURSOR_MOVE_LEFT :
            self.x -= 1
            if self.x < 0 :
                self.x = 0
        elif direction == CURSOR_MOVE_RIGHT :
            self.x += 1
            if self.x >= self.cols  :
                self.x = self.cols  - 1         

    def draw_rect(self, color) :
        cursor_rect = self.maze.get_maze_rect(self.x, self.y)
        pygame.draw.rect(gctrl.surface, color, cursor_rect)

    def draw_circle(self, color) :
        cursor_rect = self.maze.get_maze_rect(self.x, self.y)
        pygame.draw.circle(gctrl.surface, color, cursor_rect.center, 5, 2)

if __name__ == '__main__' :
    print('cursor object')