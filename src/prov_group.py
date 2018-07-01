'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''

import logging
Log = logging.getLogger('MainLogger')

class ProvGroup:
    '''ProvGroup class'''
    def __init__(self, parent, name):
        self.parent = parent
        self.name = str(name)
        self.pixels = []
        self.color_list = []
        self.marked = False

    def __repr__(self):
        i = ' '*4
        text = 'Group "'+self.name+'"\n'
        text+= i+'Pixels count: '+str(len(self.pixels))+'\n'
        text+= i+'Colors count: '+str(len(self.color_list))+'\n'
        return text[:-1]

    def get_avg_color(self):
        r, g, b = 0,0,0
        for color in self.color_list:
            r += color[0]
            g += color[1]
            b += color[2]
        r //= len(self.color_list)
        g //= len(self.color_list)
        b //= len(self.color_list)
        self.color = r,g,b
        self.color_g = self.parent._get_color_gray(self.color)
        self.color_m = self.parent._get_color_marked(self.color)

    def mark(self):
        if self.marked:
            self.marked = False
        else:
            self.marked = True
