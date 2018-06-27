'''Developed by Jakub21 in June 2018 under MIT License.
Python version: 3.6.5
Contains Bracket-File parser
'''
from PIL import Image
import yaml

import logging
Log = logging.getLogger('MainLogger')

class File:
    '''File Class
    See __init__ docs for usage
    '''
    def __init__(self, parent, path, type, is_game=False):
        '''Class constructor
        Create File object
        Parameters:
            path: [str] Specify location of a file
            type: [str] Specify file type.
                Valid types: 'yaml', 'csv', 'game', 'asgn', 'img'
            is_game: [bool] Set to true if file (def: False)
        Attributes:
            csv_separator: [str] Cell separator used in CSV files (def: ';')
            raw_read: [bool] Return raw file contents if true (def: False)
            raise_at_unknown: [bool] Defines behaviour when file type
                parameter is not recognized. When False: Return raw file
                contents. When True: Raise exception
        '''
        self.CORE, self.LOCL, self.GPATH, self.MPATH =\
            parent.CORE, parent.LOCL, parent.GPATH, parent.MPATH
        self.path, self.type, self.is_game = path, type, is_game
        self.csv_separator = ';'
        self.raw_read = False
        self.raise_at_unknown = True

    def _file_read(self, effective_path):
        try:
            return open(effective_path, 'r', encoding='utf-8-sig').read()
        except UnicodeDecodeError:
            return open(effective_path, 'r', encoding='ansi').read()

    def _clean_yaml(self, text):
        for d in range(10):
            text = text.replace(':'+str(d), ':')
        return text

    def _remove_comments(self, text):
        ndata = ''
        for line in text.split('\n'):
            nline = ''
            for c in line:
                if c in '#\r\n': break
                if c == '\t': c = ' '
                if c in '{=}': c = ' ' + c + ' '
                nline += c
            ndata += nline + ' '
        return ndata

    def _parse_yaml(self, text):
        text = self._clean_yaml(text)
        contents = yaml.load(text)
        return contents

    def _parse_csv(self, text):
        sep = self.csv_separator
        contents = text.replace('\r', '').split('\n')
        contents = [row.split(sep) for row in contents]
        return contents

    def _parse_game(self, text, rcr_depth=0):
        if type(text) == str:
            text = self._remove_comments(text)
            text = text.split()
        key_index, eql_index, val_index = 0, 1, 2
        depth = 0
        subsc_head_cut = 1
        key, value = '', ''
        in_quotes = False
        quoted_text = ''
        o_brc, c_brc, eql_sgn, quo_sgn = tuple('{}="')
        quo_sep = ' '
        index = 0
        result = {}
        subscope = []
        for word in text:
            last = False
            from_subsc = False
            if len(text) == 1:
                return text
            if word == o_brc: depth +=1
            elif word == c_brc: depth -= 1
            if (depth == 0) and (word != c_brc):
                subscope = []
            if depth != 0:
                subscope.append(word)
                continue
            if word.count(quo_sgn) == 1:
                in_quotes = not in_quotes
                if in_quotes: quoted_text = ''
                else: last = True
            if in_quotes: quoted_text += word + quo_sep
            if last: value = quoted_text + word
            if index == key_index: key = word
            elif index == eql_index:
                if word != eql_sgn: return text
            elif index == val_index:
                if not last: value = word
                if in_quotes: continue
                if value == c_brc:
                    index = (index+1)%3
                    subscope = subscope[subsc_head_cut:]
                    value = self._parse_game(subscope, rcr_depth+1)
                    from_subsc = True
                try: result[key].append(value)
                except KeyError: result[key] = [value]
            if not from_subsc: index = (index+1)%3
        return result

    def _extract_asgn(self, data):
        result = {}
        for key, mlist in data.items():
            mlist = mlist[0]
            if 'areas' in mlist: # Regn
                members = mlist['areas'][0]
            else: # Area or Segn
                o_brc, c_brc = '{', '}'
                forbidden = ['color', '=', '}']
                members = []
                depth = 0
                for memb in mlist:
                    if memb == o_brc: depth +=1
                    elif memb == c_brc: depth -= 1
                    if (memb not in forbidden) and (depth == 0):
                        try: memb = int(memb)
                        except: pass
                        members += [memb]
            result[key] = members
        return result

    def _parse(self, text, filename):
        if self.type == 'yaml':
            return self._parse_yaml(text)
        elif self.type == 'csv':
            return self._parse_csv(text)
        elif self.type == 'game':
            return self._parse_game(text)
        elif self.type == 'asgn':
            return self._extract_asgn(self._parse_game(text))
        elif self.type == 'img':
            return Image.open(filename)
        else:
            if self.raise_at_unknown:
                raise TypeError('Unknown file type "'+str(self.type)+'"')
            else:
                return text

    def read(self):
        '''Method `read` opens the file, reads and parses its contents'''
        fn = self.path
        used_fn = ''
        if self.is_game:
            fn_g = self.GPATH + fn
            fn_m = self.MPATH + fn
            try:
                text = self._file_read(fn_m)
                used_fn = fn_m
            except FileNotFoundError:
                try:
                    text = self._file_read(fn_g)
                    used_fn = fn_g
                except:
                    Log.error('File '+fn+' was not found in game/mod directory')
                    raise
        else:
            try:
                text = self._file_read(fn)
                used_fn = fn
            except FileNotFoundError:
                Log.error('File '+fn+' was not found (base dir)')
                raise
        if self.raw_read:
            return text
        contents = self._parse(text, used_fn)
        self.contents = contents
        return contents
