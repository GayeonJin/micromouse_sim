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
from cursor import *
from maze import *
from mouse import *

INFO_HEIGHT = 40
INFO_OFFSET = 10
INFO_FONT = 20

def draw_step(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Step : " + str(count), True, COLOR_WHITE)
    gctrl.surface.blit(text, (gctrl.width - 100, 0))

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def draw_info(mode) :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    if mode == 'edit' :
        info = font.render('F1/F2 : load/save map   a/d/s/w : left/right/down/up    x : exit', True, COLOR_BLACK)
    elif mode == 'run' :
        info = font.render('space : go', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.surface, COLOR_GRAY, (0, gctrl.height - INFO_HEIGHT, gctrl.width, INFO_HEIGHT))
    gctrl.surface.blit(info, (INFO_OFFSET * 2, gctrl.height - INFO_FONT - INFO_OFFSET))

def terminate() :
    pygame.quit()
    sys.exit()

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
                elif event.key == pygame.K_F1 :               
                    maze.load()
                elif event.key == pygame.K_F2 :
                    maze.save()
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
                x, y = maze.get_pos(mouse_pos)
                if x != None or y != None :
                    cursor.set_pos(x, y) 

        # Move cursor
        if direction != 0 :
            cursor.move(direction)
            direction = 0

        # Change wall
        if edit_wall != 0 : 
            maze.edit_wall(cursor.x, cursor.y, edit_wall)
            edit_wall = 0
            
        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Draw maze
        maze.draw()

        # Draw cursor
        cursor.draw_circle(COLOR_BLACK)

        # Draw Info
        draw_info('edit')

        pygame.display.update()
        clock.tick(60)

def run_mouse() :
    global clock
    global maze, mouse

    maze.load()

    auto = False
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
                if event.key == pygame.K_SPACE:
                    mouse.set_state(MOUSE_STATE_SEARCH_GOAL)                    
                elif event.key == pygame.K_x :
                    return

        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Move mouse
        if dir != 0 :
            mouse.move(dir)

        if auto == True :
            state = mouse.is_state()
            if state == MOUSE_STATE_BACK_TO_START :
                mouse.move_to_start()
            elif state == MOUSE_STATE_FIND_GOAL:
                mouse.set_state(MOUSE_STATE_BACK_TO_START)
            else :
                wall = mouse.sense_wall()
 
                mouse.move_auto(wall)
                mouse.move_to_next_path()                
                mouse.move_to_branch()

        auto = False

        # Draw maze
        maze.draw()

        # Draw mouse
        mouse.draw_map_prohibit()
        mouse.draw()

        pygame.display.update()
        clock.tick(60)

def run_mouse_auto() :
    global clock
    global maze, mouse

    maze.load()
    mouse.init_variables()

    simulation_end = False
    auto = True
    run_end = False
    while not run_end :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run_end = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_SPACE:
                    mouse.set_state(MOUSE_STATE_SEARCH_GOAL)

        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Move mouse
        if auto == True :
            state = mouse.is_state()
            if state == MOUSE_STATE_BACK_TO_START :
                if mouse.move_to_start() == True :
                    simulation_end = True
                    auto = False
            elif state == MOUSE_STATE_FIND_GOAL:
                mouse.set_state(MOUSE_STATE_BACK_TO_START)
            else :
                wall = mouse.sense_wall()
 
                mouse.move_auto(wall)
                mouse.move_to_next_path()                
                mouse.move_to_branch()

        # Draw maze
        maze.draw()

        # Draw mouse
        mouse.draw_map_prohibit()
        mouse.draw()

        if mouse.is_state() == MOUSE_STATE_FIND_GOAL :
            draw_message('Find Goal')

        # Draw Info
        draw_info('run')

        pygame.display.update()
        clock.tick(10)

        if simulation_end == True :
            draw_message('Arrive at start point')
            return

def start_mouse() :
    # Clear surface
    gctrl.surface.fill(COLOR_WHITE)

    bg_img = pygame.image.load('image/mouse_bg.png')
    # bg_img = pygame.transform.scale_by(bg_img, 0.6)

    bg_rect = bg_img.get_rect()
    bg_rect.left = gctrl.width - bg_rect.width
    bg_rect.top = gctrl.height - bg_rect.height
    gctrl.surface.blit(bg_img, bg_rect)

    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render("Micro Mouse Simulator", True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    gctrl.surface.blit(text_suf, text_rect)

    help_str = ['e : edit maze',
                'g : go mouse',
                't : test mouse',
                'x : exit simualtion']

    font1 = pygame.font.SysFont(None, 30)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.width / 2
        gctrl.surface.blit(text_suf1, text_rect1)

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

    # mouse
    mouse = mouse_object(maze)

    (pad_width, pad_height) = maze.get_padsize()
    pad_height += INFO_HEIGHT
    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
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

