#!/usr/bin/python

import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

resource_path = ''

resource_image = {
    'id_background' : 'image/mouse_bg.png',
    'id_mouse' : 'image/mouse.png'
}

def get_img_resource(resource_id) :
    return resource_path + resource_image[resource_id]

if __name__ == '__main__' :
    print('resoure')