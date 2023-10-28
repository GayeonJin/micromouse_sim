#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from gobject import *
from maze import *

MOUSE_SIZE = 5

MOUSE_MOVE_LEFT = 1
MOUSE_MOVE_DOWN = 2
MOUSE_MOVE_RIGHT = 4
MOUSE_MOVE_UP = 8

MOUSE_TYPE_CIRCLE = 1
MOUSE_TYPE_IMG = 2

MOUSE_NORMAL = 1
MOUSE_RETURN = 2

MOUSE_STATE_IDLE = 1
MOUSE_STATE_SEARCH_GOAL = 2
MOUSE_STATE_BACK_TO_BRANCH = 3
MOUSE_STATE_MOVE_TO_NEXT = 4
MOUSE_STATE_FIND_GOAL = 5
MOUSE_STATE_BACK_TO_START = 6
MOUSE_STATE_ARRIVE = 7

class mouse_object :
    def __init__(self, maze) :
        self.maze = maze
        self.rows, self.cols = self.maze.get_size()

        self.goal_count = 0
        self.goals = []
        self.goals.append([self.maze.cols / 2 - 1, self.maze.rows / 2 - 1])
        self.goals.append([self.maze.cols / 2 - 1, self.maze.rows / 2])
        self.goals.append([self.maze.cols / 2, self.maze.rows / 2 - 1])
        self.goals.append([self.maze.cols / 2, self.maze.rows / 2])

        self.trace = []
        self.branch = []
        self.map = []
        
        self.mouse_obj = game_object(0, 0, get_img_resource('id_mouse'))
        self.mouse_obj1 = game_object(0, 0, get_img_resource('id_mouse1'))

        self.init_variables()

    def init_variables(self) :
        self.x = 0
        self.y = 0
        self.dir = MOUSE_MOVE_UP

        self.trace.clear()
        self.trace.append([self.x, self.y])

        self.branch.clear()

        self.map.clear()
        self.rows, self.cols = self.maze.get_size()
        for x in range(self.cols) :
            self.map.append([])
            for y in range(self.rows) :
                self.map[x].append(0)

        self.goal_count = 0

        self.branch_dest = None
        self.branch_next = None
        self.state = MOUSE_STATE_IDLE
        
    def set_state(self, state) :
        self.state = state

    def is_state(self) :
        return self.state

    def update_map(self, x, y, wall) :
        self.map[x][y] = wall

    def get_cur_pos(self) :
        return [self.x, self.y]
    
    def get_next_pos(self, direction) :
        x = self.x
        y = self.y
        if direction == MOUSE_MOVE_UP:
            y += 1
        elif direction == MOUSE_MOVE_DOWN :
            y -= 1
        elif direction == MOUSE_MOVE_LEFT :
            x -= 1
        elif direction == MOUSE_MOVE_RIGHT :
            x += 1

        return [x, y]

    def get_direction(self, cur_pos, next_pos) :
        if (cur_pos[0] == next_pos[0]) :
            if cur_pos[1] < next_pos[1] :
                return MOUSE_MOVE_UP
            else :
                return MOUSE_MOVE_DOWN
        else :
            if cur_pos[0] < next_pos[0] :
                return MOUSE_MOVE_RIGHT
            else :
                return MOUSE_MOVE_LEFT   

    def check_goal(self) :
        for goal in self.goals :
            if goal == [self.x, self.y] :
                self.goal_count += 1
                if self.goal_count == 4 :
                    print("find goal")
                    print(self.trace)
                    self.state = MOUSE_STATE_FIND_GOAL
                    return True

        return False        

    def get_entrance(self) :
        if self.dir == MOUSE_MOVE_LEFT :
            entrance = WALL_RIGHT
        elif self.dir == MOUSE_MOVE_RIGHT :
            entrance = WALL_LEFT
        elif self.dir == MOUSE_MOVE_UP :
            entrance = WALL_BOTTOM
        elif self.dir == MOUSE_MOVE_DOWN :
            entrance = WALL_TOP
        return entrance

    def check_branch(self, wall) :
        entrance = self.get_entrance()
        if wall & entrance != 0 :
            wall_filter = WALL_ALL
        else :
            wall_filter = WALL_ALL & ~entrance

        next_pos = []
        gate = wall ^ wall_filter
        if gate != 0 : 
            if gate & WALL_LEFT :
                next_pos.append(self.get_next_pos(MOUSE_MOVE_LEFT))
            if gate & WALL_BOTTOM :
                next_pos.append(self.get_next_pos(MOUSE_MOVE_DOWN))
            if gate & WALL_RIGHT :
                next_pos.append(self.get_next_pos(MOUSE_MOVE_RIGHT))
            if gate & WALL_TOP :
                next_pos.append(self.get_next_pos(MOUSE_MOVE_UP))

        print('check branch : ', next_pos)

        if len(next_pos) >= 1 :
            res_pos = next_pos.pop(0)

            if len(next_pos) :
                for i, pos in enumerate(next_pos) :
                    self.branch.append([self.get_cur_pos(), pos])
                    print('save the next path : ', pos)

            return res_pos
    
        return None

    def check_next_path(self, wall) :
        entrance = self.get_entrance()

        wall_filter = WALL_ALL & ~entrance

        if wall ^ wall_filter == 0 :
            print("no next path, back to branch")
            self.state = MOUSE_STATE_BACK_TO_BRANCH
            return False
        else :
            return True

    def sense_wall(self) :
        wall = self.maze.get_wall(self.x, self.y)
        return wall

    def move_next(self, direction, trace = True) :
        if direction == MOUSE_MOVE_UP:
            self.y += 1
        elif direction == MOUSE_MOVE_DOWN :
            self.y -= 1
        elif direction == MOUSE_MOVE_LEFT :
            self.x -= 1
        elif direction == MOUSE_MOVE_RIGHT :
            self.x += 1

        self.dir = direction
        if trace == True :
            self.trace.append([self.x, self.y])

    def move_to_branch(self) :
        if self.state != MOUSE_STATE_BACK_TO_BRANCH : 
            return False
        
        if self.branch_dest == None :
            self.branch_dest, self.branch_next = self.branch.pop()
            print("go back", self.branch_dest, self.branch_next)

        print(self.get_cur_pos())
        print(self.trace)

        next_pos = self.trace.pop()
        if self.x == next_pos[0] and self.y == next_pos[1] :
            self.update_map(next_pos[0], next_pos[1], WALL_ALL) 
            next_pos = self.trace.pop()

        direction = self.get_direction(self.get_cur_pos(), next_pos)
        
        if self.branch_dest == next_pos :
            self.move_next(direction)
            self.state = MOUSE_STATE_MOVE_TO_NEXT
        else :
            self.move_next(direction, False)
            self.update_map(next_pos[0], next_pos[1], WALL_ALL) 
        
        return True

    def move_to_next_path(self) :
        if self.state != MOUSE_STATE_MOVE_TO_NEXT :
            return
        
        # move next pos
        direction = self.get_direction(self.get_cur_pos(), self.branch_next)
        self.move_next(direction)

        print("go to new path", self.branch_next)

        self.branch_dest = None
        self.branch_next = None
        self.state = MOUSE_STATE_SEARCH_GOAL 

    def move_to_start(self) :
        if self.state != MOUSE_STATE_BACK_TO_START :
            return False
        
        next_pos = self.trace.pop()
        if self.x == next_pos[0] and self.y == next_pos[1] :
            next_pos = self.trace.pop()

        direction = self.get_direction(self.get_cur_pos(), next_pos)
        self.move_next(direction, False)

        if len(self.trace) == 0 :
            self.dir = MOUSE_MOVE_UP
            self.state = MOUSE_STATE_ARRIVE
            return True
        
        return False

    def move_auto(self, wall) :
        if self.state != MOUSE_STATE_SEARCH_GOAL :
            return False 

        next_pos = self.check_branch(wall)
        if next_pos == None :
            self.check_next_path(wall)
            return False

        direction = self.get_direction(self.get_cur_pos(), next_pos)

        if (wall & direction) == 0 :
            self.move_next(direction)
            self.update_map(self.x, self.y, wall)

            self.check_goal()
                
            if self.state == MOUSE_STATE_FIND_GOAL :    
                return True
        
        return False

    def move(self, direction) :
        wall = self.maze.get_wall(self.x, self.y)

        if (wall & direction) == 0 :
            self.move_next(direction)
            self.update_map(self.x, self.y, wall)
            
            # check wall of next pos
            wall = self.maze.get_wall(self.x, self.y)
            self.check_branch(wall)

            self.check_next_path(wall)
 
            # check goal
            self.check_goal()

            return True
        else :
            return False

    def draw_mouse(self, type = MOUSE_TYPE_CIRCLE, mode = MOUSE_NORMAL, color = COLOR_BLACK) :
        maze_rect = self.maze.get_maze_rect(self.x, self.y)

        if type == MOUSE_TYPE_CIRCLE :
            pygame.draw.circle(gctrl.gamepad, color, maze_rect.center, MOUSE_SIZE, 2)
        elif type == MOUSE_TYPE_IMG :
            rotate_angle = 0
            if self.dir == MOUSE_MOVE_LEFT :
                rotate_angle = 90
            elif self.dir == MOUSE_MOVE_RIGHT :
                rotate_angle = 270
            elif self.dir == MOUSE_MOVE_DOWN :
                rotate_angle = 180

            if mode == MOUSE_NORMAL :
                self.mouse_obj.draw_rect(maze_rect, rotate_angle)
            elif mode == MOUSE_RETURN :
                self.mouse_obj1.draw_rect(maze_rect, rotate_angle)

    def draw_map_prohibit(self) :
        for y in range(self.rows) :
            for x in range(self.cols) :
                if self.map[x][y] == WALL_ALL :
                    maze_rect = self.maze.get_maze_rect(x, y)
                    pygame.draw.circle(gctrl.gamepad, COLOR_BLUE, maze_rect.center, 1, 2)                    

    def draw(self) :
        maze_rect = self.maze.get_maze_rect(self.x, self.y)
        if self.state == MOUSE_STATE_BACK_TO_BRANCH :
            self.draw_mouse(MOUSE_TYPE_IMG, MOUSE_RETURN)
        else :
            self.draw_mouse(MOUSE_TYPE_IMG, MOUSE_NORMAL)
            # self.draw_mouse(MOUSE_TYPE_CIRCLE, COLOR_RED)

if __name__ == '__main__' :
    print('mouse object')