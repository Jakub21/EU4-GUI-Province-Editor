'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''

def init_prov_file(core, locl):
    '''Copy global variables to this file
    Prevents repeating long construct lines of Province class
    TODO: Find a way to do this w/o this function
    '''
    global CORE, LOCL
    CORE, LOCL = core, locl


class Province:
    '''Province'''
    def __init__(self, parent, id, name, type):
        try: # Copy globals
            self.CORE, self.LOCL = CORE, LOCL
        except:
            raise TypeError('Please call init_prov_file function first')
        self.parent, self.id, self.name, self.type = parent, id, name, type
        self.marked = False

    def __repr__(self):
        i = ' '*4
        text = 'Province '+str(self.id)+' "'+self.name+'"\n'
        text += i+'Type: '+str(self.type)+'\n'
        try:
            text += i+'Color: '+str(self.color)
            text += ' [gray: '+str(self.color_g)
            text += ' marked:'+str(self.color_m)+']\n'
        except AttributesError: text += 'Colors not set\n'
        try:
            text += i+'Assignment: '+str(self.segn)+'/'
            text += str(self.regn)+'/'+str(self.area)+'\n'
        except AttributeError: text += 'Assignment not set\n'
        return text[:-1]

    def set_color(self, id_color, gray_color, marked_color):
        self.color = id_color
        self.color_g = gray_color
        self.color_m = marked_color

    def mark(self):
        if self.marked:
            self.marked = False
            self.parent._update_map(self.pixels, self.color_g)
        else:
            self.marked = True
            self.parent._update_map(self.pixels, self.color_m)

    def set_pixels(self, pixels):
        self.pixels = pixels

    def assign(self, area, regn, segn):
        self.area = area.replace('_area','')
        self.regn = regn.replace('_region','')
        self.segn = segn.replace('_superregion','')

    def set_history(self, data):
        '''Generate history data from parsed history file contents'''
        def get_date(text):
            try:
                y, m, d = [int(el) for el in text.split('.')]
                return (y,m,d)
            except:
                return False

        #if self.id != 118: return # TEMP
        undefined = []
        for fkey, value in data.items():
            if fkey in self.CORE['val-keys'].keys():
                key = self.CORE['val-keys'][fkey]
            elif fkey in self.CORE['add-keys'].keys():
                key = self.CORE['add-keys'][fkey]
            elif fkey in self.CORE['rem-keys'].keys():
                key = self.CORE['rem-keys'][fkey]
            else:
                date = get_date(fkey)
                if not date:
                    undefined.append(fkey)
                    continue
                self.set_history(data[fkey][0])

        self.parent.undefined += undefined

        # TODO
