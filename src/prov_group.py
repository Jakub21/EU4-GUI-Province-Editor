'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
from src.chunk import Chunk

class ProvGroup(Chunk):
    '''Province Group Class'''
    def __init__(self, parent, name, type):
        '''Constructor'''
        super().__init__(parent, name, type)
        self.members = []

    def __repr__(self):
        '''Generates repr string of the object'''
        i = ' '*4
        text = 'ProvGroup'
        text += super().__repr__()[len('chunk'):]
        text += i + 'Members count: '+str(len(self.members))+'\n'
        return text

    def mark(self, modify_map=True, force=None):
        '''Marks or Unmarks the group.
        To skip map update set modify_map to False.
        To force state of marked attr. use force parameter.
        Silently updates marked attr. of all member provinces
        '''
        super().mark(modify_map, force)
        for prov in self.members:
            id = prov.id
            self.parent.provs[id].mark(modify_map='provs', force=self.marked)

    def mark_members(self, force=None):
        state = self.marked
        if force in (True, False):
            state = force
        for prov in self.members:
            id = prov.id
            self.parent.provs[id].mark(modify_map='provs', force=state)

    def get_mem_pixels(self):
        '''Get pixels from the members'''
        for member in self.members:
            self.pixels += member.pixels

    def set_members(self, members):
        '''Sets members of the group'''
        self.members = members

    def add_member(self, member):
        '''Add single province to member list'''
        self.members += [member]

    def calc_avg_color(self):
        '''Calculates average "identifier" color of members'''
        r, g, b = 0, 0, 0
        amount = len(self.members)
        for member in self.members:
            mr, mg, mb = member.color
            r += mr
            g += mg
            b += mb
        r //= amount
        g //= amount
        b //= amount
        return r,g,b
