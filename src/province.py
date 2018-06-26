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

    def _get_date(self, text):
        try:
            y, m, d = [int(el) for el in text.split('.')]
            return (y,m,d)
        except: return False

    def _get_hist_default(self):
        history = {}
        for fkey, pkey in self.CORE['bln-fkeys'].items():
            history[pkey] = False
        for fkey, pkey in self.CORE['spc-fkeys'].items():
            history[pkey] = ''
        for fkey, pkey in self.CORE['num-fkeys'].items():
            history[pkey] = 0
        for fkey, pkey in self.CORE['add-fkeys'].items():
            history[pkey] = ''
        return history

    def _get_scope(self, data):
        history = {}
        for fkey, pkey in self.CORE['bln-fkeys'].items():
            try:
                if data[fkey][0] == 'yes':
                    history[pkey] = True
                else:
                    history[pkey] = False
            except KeyError: pass
        for fkey, pkey in self.CORE['spc-fkeys'].items():
            try:
                history[pkey] = data[fkey][0]
            except KeyError: pass
        for fkey, pkey in self.CORE['num-fkeys'].items():
            try:
                history[pkey] = int(data[fkey][0])
            except KeyError: pass
            # TODO: except TypeError: ?
        for fkey, pkey in self.CORE['add-fkeys'].items():
            try:
                history[pkey] += data[fkey]
            except KeyError:
                try:
                    history[pkey] = data[fkey]
                except KeyError: pass
        for fkey, pkey in self.CORE['rem-fkeys'].items():
            try:
                history[pkey] = [i for i in history[pkey] \
                    if i not in data[fkey]]
            except KeyError:
                pass
        for category, bld_list in self.CORE['bld-fkeys'].items():
            for building in bld_list:
                try:
                    if data[building] == 'yes':
                        history[category] = category.index(building)+1
                except KeyError: pass
        return history

    def _is_earlier(self, date_a, date_b):
        '''Return True if date_a is earlier than date_b (or equal)'''
        if date_a == date_b: return True
        ya, ma, da = date_a
        yb, mb, db = date_b
        if ya < yb:
            return True
        elif ya == yb:
            if ma < mb:
                return True
            elif ma == mb:
                if da < db:
                    return True
        return False

    def set_history(self, data):
        '''Generate history data from parsed history file contents'''
        limit = self.parent.DATE
        self.history = self._get_hist_default()
        self.history.update(self._get_scope(data))
        for date, subdata in data.items():
            date = self._get_date(date)
            if not date: continue
            if self._is_earlier(date, limit):
                date_hist = self._get_scope(subdata[0])
                self.history.update(date_hist)
