'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''

class Chunk:
    '''Chunk Class
    Contains methods inherited by ProvGroup and Province classes
    '''
    def __init__(self, parent, name, type):
        '''Constructor'''
        self.parent, self.name, self.type = parent, name, type
        self.marked = False
        self.pixels = []

    def __repr__(self):
        '''Generates repr string of the object'''
        i = ' '*4
        text = 'Chunk "'+str(self.name)+'"\n'
        text += i + 'Type: '+str(self.type)+'\n'
        text += i + 'Is marked: '+str(self.marked)+'\n'
        text += i + 'Pixels count: '+str(len(self.pixels))+'\n'
        try:
            text += i+'Colors: '+str([self.color, self.g_clr, self.m_clr])+'\n'
        except AttributeError: text += i + 'Colors not set\n'
        return text

    def set_pixels(self, pixels):
        '''Sets pixels of the chunk'''
        self.pixels = pixels

    def set_color(self, color):
        '''Sets chunk colors. Pass identifier color as a parameter.
        Marked and Grayed colors are calculated by helper methods.
        '''
        self.color = color
        self.g_clr = self._get_gray(color)
        self.m_clr = self._get_marked(color)

    def mark(self, modify_map=True, force=None):
        '''Marks or Unmarks the chunk.
        To skip map update set modify_map to False.
        To force state of marked attr. use force parameter.
        '''
        color = {
            True: self.m_clr,
            False: self.g_clr,
        }
        if force in (True, False):
            self.marked = force
        else:
            self.marked = not self.marked
        if modify_map:
            self.parent.mark_chunk(self.pixels, color[self.marked])

    # set_color helper methods

    def _get_gray(self, color):
        r, g, b = color
        r = (r+100)//4
        g = (g+100)//4
        b = (b+100)//4
        return r, g, b

    def _get_marked(self, color):
        r, g, b = color
        r = (r+510)//3
        g = (g+510)//3
        b = (b+510)//3
        return r, g, b
