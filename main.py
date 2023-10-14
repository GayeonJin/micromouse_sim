#!/usr/bin/python

import os
import sys
import csv

import pygame
import random
from time import sleep

from tkinter import filedialog
from tkinter import *

from gresource import *
from gobject import *
from cursor import *
from maze import *
from mouse import *

def draw_step(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Step : " + str(count), True, COLOR_WHITE)
    gctrl.gamepad.blit(text, (gctrl.pad_width - 100, 0))

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))

    gctrl.gamepad.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def draw_cursor(x, y) :
    maze_rect = maze.get_maze_rect(x, y)
    pygame.draw.circle(gctrl.gamepad, COLOR_BLACK, maze_rect.center, MOUSE_SIZE, 2)

def edit_maze() :
    global root
    global clock
    global maze

    cursor = cursor_object(maze)

    cursor.x = 0
    cursor.y = 0
    direction =0

    edit_wall = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_a:
                    edit_wall = WALL_LEFT
                elif event.key == pygame.K_s :
                    edit_wall = WALL_BOTTOM
                elif event.key == pygame.K_d :
                    edit_wall = WALL_RIGHT
                elif event.key == pygame.K_w :
                    edit_wall = WALL_TOP
                elif event.key == pygame.K_1 :               
                    maze.load()
                elif event.key == pygame.K_2 :
                    maze.save()
                elif event.key == pygame.K_x :
                    return

        # Move cursor
        cursor.move(direction)
        direction = 0

        # Change wall
        maze.edit_wall(cursor.x, cursor.y, edit_wall)
        edit_wall = 0
            
        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

        # Draw maze
        maze.draw()

        # Draw cursor
        cursor.draw_circle(COLOR_BLACK)

        pygame.display.update()
        clock.tick(60)

def run_mouse() :
    global clock
    global maze, mouse

    maze.load()

    run_end = False
    while not run_end :
        dir = 0
        auto = False
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run_end = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    dir = MOUSE_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    dir = MOUSE_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    dir = MOUSE_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    dir = MOUSE_MOVE_RIGHT
                elif event.key == pygame.K_r :
                    auto = True
                elif event.key == pygame.K_x :
                    return

        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

        # Move mouse
        if dir != 0 :
            mouse.move(dir)

        if auto == True :
            if mouse.goto_start == False :
                wall = mouse.sense_wall()
 
                if mouse.check_next_path(wall) == False :
                    mouse.move_to_branch()
                else :
                    mouse.move_auto(wall)
            else :
                mouse.move_to_start()

        # Draw maze
        maze.draw()

        # Draw mouse
        mouse.draw_map_prohibit()
        mouse.draw()

        pygame.display.update()
        clock.tick(60)
    
    print('run_mouse : end')

def run_mouse_auto() :
    global clock
    global maze, mouse

    maze.load()

    simulation_end = False
    auto = True
    run_end = False
    while not run_end :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run_end = True

        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

        # Move mouse
        if auto == True :
            if mouse.goto_start == False :
                wall = mouse.sense_wall()
 
                if mouse.check_next_path(wall) == False :
                    mouse.move_to_branch()
                else :
                    mouse.move_auto(wall)

                if mouse.goto_start == True :
                    draw_message('Find Gole')
            else :
                if mouse.move_to_start() == True :
                    simulation_end = True
                    auto = False

        # Draw maze
        maze.draw()

        # Draw mouse
        mouse.draw_map_prohibit()
        mouse.draw()

        pygame.display.update()
        clock.tick(10)

        if simulation_end == True :
            draw_message('Arrive Start')
            return

def start_mouse() :
    # Clear gamepad
    gctrl.gamepad.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render("Micro Mouse Simulator", True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))
    gctrl.gamepad.blit(text_suf, text_rect)

    help_str = ['e : edit maze',
                'g : go mouse',
                't : test mouse',
                'x : exit simualtion']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.pad_width / 2
        gctrl.gamepad.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_e :
                    return 'edit'
                elif event.key == pygame.K_g :
                    return 'run'
                elif event.key == pygame.K_t :
                    return 'test'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_mouse() :
    global root
    global clock
    global maze, mouse

    pygame.init()
    clock = pygame.time.Clock()

    # maze
    maze = maze_object(MAX_ROWS, MAX_COLS)
    (pad_width, pad_height) = maze.get_padsize()
    mouse = mouse_object(maze)

    gctrl.set_param(pygame.display.set_mode((pad_width, pad_height)), pad_width, pad_height)
    pygame.display.set_caption("Micro Mouse Simulator")

if __name__ == '__main__' :
    init_mouse()
    while True :
        mode = start_mouse()
        if mode == 'edit' :
            edit_maze()
        elif mode == 'run' :
            run_mouse_auto()
        elif mode == 'test' :
            run_mouse()
