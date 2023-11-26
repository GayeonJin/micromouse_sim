#!/usr/bin/python

import sys
import time
import pygame

COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

resource_path = ''

resource_image = {
    'id_background' : 'image/mouse_bg.png',
    'id_mouse' : 'image/mouse.png',
    'id_mouse1' : 'image/mouse1.png'
}

def get_img_resource(resource_id) :
    return resource_path + resource_image[resource_id]

ALIGN_LEFT = 0x01
ALIGN_RIGHT = 0x02
ALIGN_CENTER = 0x04
ALIGN_BOTTOM = 0x10
ALIGN_TOP = 0x20

FPS = 60

class game_ctrl :
    def __init__(self) :
        self.surface = None 
        self.width = 640
        self.height = 320

        pygame.init()
        self.clock = pygame.time.Clock()

    def set_surface(self, surface) :
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

    def save_scr_capture(self, prefix) :
        pygame.image.save(self.surface,(prefix + time.strftime('%Y%m%d%H%M%S')+ '.jpg'))

    def draw_string(self, str, x_offset = 0, y_offset = 0, align = ALIGN_LEFT, font_size = 25, font_color = COLOR_WHITE) :
        font = pygame.font.SysFont(None, font_size)
        text = font.render(str, True, font_color)
        text_rect = text.get_rect()

        text_rect.top = y_offset
        if align & ALIGN_LEFT :
            text_rect.left = x_offset    
        elif align & ALIGN_RIGHT :
            text_rect.left = self.width - text_rect.width - x_offset
        elif align & ALIGN_CENTER :
            text_rect.center = ((self.width / 2), (self.height / 2))

        if align & ALIGN_TOP :
            text_rect.top = y_offset
        elif align & ALIGN_BOTTOM :
            text_rect.top = self.height - y_offset
            
        self.surface.blit(text, text_rect)

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('main surface and resource')