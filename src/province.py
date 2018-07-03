'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
from src.chunk import Chunk

class Province(Chunk):
    '''Province Class'''
    def __init__(self, parent, name, type, id):
        '''Constructor'''
        super().__init__(parent, name, type)
        self.CORE, self.LOCL = parent.CORE, parent.LOCL
        self.id = id

    def __repr__(self):
        '''Generates repr string of the object'''
        i = ' '*4
        text = 'Province #'+str(self.id)
        text += super().__repr__()[len('chunk'):]
        try:
            text += i + 'Assignment: '+str(self.segn)+' / '
            text += str(self.regn) + ' / ' + str(self.area) + '\n'
        except AttributeError: text += i + 'Assignment not set\n'
        try:
            text += i + 'History file name: '+str(self.filename)+'\n'
        except AttributeError: text += i + 'History file name not set\n'
        try:
            s = max([len(str(key)) for key in self.history.keys()])
            text += i + 'Province history data:\n'
            for key, value in self.history.items():
                text += i*2+str(key)+' '*(s-len(key))+' : '+str(value)+'\n'
        except AttributeError: text += i + 'History data not loaded\n'
        return text

    def assign(self, area, regn, segn):
        '''Sets region assignment of the province'''
        self.area, self.regn, self.segn = area, regn, segn

    def set_history(self, data, fn):
        '''Generate history data from parsed history file contents
        Additionally set province's history file name
        '''
        self.filename = fn
        limit = self.parent.DATE
        self.history = self._get_scope(data, self._get_hist_default())
        for date, subdata in data.items():
            date = self._get_date(date)
            if not date: continue
            if self._is_earlier(date, limit):
                self.history = self._get_scope(subdata[0], self.history)

    # set_history helper methods

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
            history[pkey] = []
        for category in self.CORE['bld-fkeys'].keys():
            history[category] = 0
        return history

    def _get_scope(self, data, history):
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
                    if data[building] == ['no']:
                        history[category] = 0
                    if data[building] == ['yes']:
                        history[category] = bld_list.index(building)+1
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
