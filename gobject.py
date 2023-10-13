#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

INIT_POS_LEFT = 0
INIT_POS_RIGHT = 1

class game_ctrl :
    def __init(self) :
        self.gamepad = None 
        self.pad_width = 640
        self.pad_height = 320

    def set_param(self, pad, width, height) :
        self.gamepad = pad
        self.pad_width = width
        self.pad_height = height

class game_object :
    global gctrl

    def __init__(self, x, y, resource_path) :
        if resource_path != None :
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.life_count = 1

    def init_position(self, mode) :
        if mode == INIT_POS_LEFT :
            self.set_position(gctrl.pad_width * 0.05, gctrl.pad_height / 2)
        elif mode == INIT_POS_RIGHT :
            self.set_position(gctrl.pad_width, random.randrange(0, gctrl.pad_height - self.height))

    def set_position(self, x, y) : 
        self.x = x
        self.y = y        
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1
        
    def move(self, del_x, del_y) :
        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (gctrl.pad_height - self.height) :
            self.y = (gctrl.pad_height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.gamepad.blit(self.object, (self.x, self.y))            

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.pad_width :
            return True
        else :
            return False

    def is_life(self) :
        if self.life_count > 0 :
            return True
        else :
            return False
    
    def set_life_count(self, count) :
        self.life_count = count
        if self.life_count > 0 :
            self.life = True

    def get_life_count(self) :
        return self.life_count
    
    def kill_life(self) :
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy_item) :
        if self.object != None and enemy_item.object != None :
            if self.ex > enemy_item.x :
                if (self.y > enemy_item.y and self.y < enemy_item.ey) or (self.ey > enemy_item.y and self.ey < enemy_item.ey) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy_item.x, enemy_item.y, enemy_item.ex, enemy_item.ey)
                    return True
        return False

class backgroud_object(game_object) :
    def __init__(self, resource_path) :
        self.object = pygame.image.load(resource_path)
        self.object2 = self.object.copy()

        self.width = self.object.get_width()
        self.height = self.object.get_height()

        self.x = 0
        self.x2 = self.width
        self.scroll_width = -2

    def scroll(self) :
        self.x += self.scroll_width
        self.x2 += self.scroll_width

        if self.x == -self.width:
            self.x = self.width

        if self.x2 == -self.width:
            self.x2 = self.width

    def draw(self) :
        gctrl.gamepad.blit(self.object, (self.x, 0))
        gctrl.gamepad.blit(self.object2, (self.x2, 0))

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('game control and object')