#!/usr/bin/python

import sys

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

class game_ctrl :
    def __init__(self) :
        self.surface = None 
        self.width = 640
        self.height = 320

    def set_surface(self, surface) :
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('main surface and resoure')