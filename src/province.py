'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''

class Province:
    '''Province'''
    def __init__(self, parent, id, name, type):
        self.parent, self.id, self.name, self.type = parent, id, name, type
        self.CORE, self.LOCL = parent.CORE, parent.LOCL
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
            self.parent.mark_prov_map(self.pixels, self.color_g)
        else:
            self.marked = True
            self.parent.mark_prov_map(self.pixels, self.color_m)

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

        undefined = []
        for fkey, value in data.items():
            found = False
            for category in ['bln-fkeys', 'spc-fkeys', 'num-fkeys',
                'add-fkeys', 'rem-fkeys']:
                if fkey in self.CORE[category].keys():
                    key = self.CORE[category][fkey]
                    found = True
            for category, bld_list in self.CORE['bld-fkeys'].items():
                if fkey in bld_list:
                    found = True
            if not found:
                date = get_date(fkey)
                if not date:
                    undefined.append(fkey)
                    continue
                self.set_history(data[fkey][0])

        # TODO
