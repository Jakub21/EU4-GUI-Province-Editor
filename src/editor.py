'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
import yaml
from PIL import Image
from os import listdir
from src.gui import MainFrame
from src.province import Province
from src.file import File

import logging
Log = logging.getLogger('MainLogger')

class Editor(MainFrame):
    '''Parses game files'''
    def __init__(self):
        Log.info('Loading config')
        self.load_config()
        super().__init__(self.CORE, self.LOCL)

        Log.info('Reading game data')
        self.set_busy_on(key='msg-loading-data')
        self.load_game_data()
        self.create_provs()

        Log.info('Loading history data')
        self.set_busy_on(key='msg-loading-hist')
        self.load_history()

        Log.info('Loading map')
        self.set_busy_on(key='msg-loading-map')
        self.MAP = self.PROV_MAP
        self.init_gui()
        self.mapmode_provs()
        self.Center()
        self.isBusy = False
        Log.info('Done')
        self.set_busy_off()
        self.Show()

    def load_config(self):
        USER_CONFIG_PATH = 'config/user.yml'
        CORE_CONFIG_PATH = 'config/core.yml'
        LOCALISATION_PATH = 'config/lang.yml'

        USER = yaml.load(open(USER_CONFIG_PATH, 'r').read())
        self.GPATH = USER['game-path'].replace('\\', '/')
        self.MPATH = self.GPATH + '/mod' + USER['mod-name'].replace('\\', '/')
        self.LANG = USER['lang']
        self.SCALE = USER['default-zoom']

        self.CORE = open(CORE_CONFIG_PATH, 'r').read()
        self.CORE = self.CORE.replace('$LANG$', USER['lang'])
        self.CORE = yaml.load(self.CORE)
        self.DATE = self.CORE['default-date']

        self.LOCL = open(LOCALISATION_PATH, 'r').read()
        self.LOCL = yaml.load(self.LOCL)

    def load_game_data(self):
        mapdef = self._load_map_def()
        self.MAP_SIZE, self.SEA_PROVS, self.RNW_PROVS, self.LAKE_PROVS = mapdef
        self.COLOR_DEFS = self._load_clr_def()
        self.ID_POS, self.PROV_MAP = self._load_prov_map()
        self.PROV_NAMES = self._load_localisation()
        self.ASSIGNMENT = self._load_assignment()

    def load_history(self):
        history = {}
        namelist = []
        subdir = self.CORE['path']['prov-hist-dir']
        try:
            namelist = listdir(self.MPATH+subdir)
        except FileNotFoundError: pass
        try:
            namelist += listdir(self.GPATH+subdir)
        except FileNotFoundError: pass
        namelist = list(set(namelist))
        for fn in namelist:
            file = File(self, subdir+fn, 'game', True)
            contents = file.read()
            id = self._get_id(fn)
            self.provs[id].set_history(contents, fn)

    def create_provs(self):
        undefined = 'Undefined'
        provinces = {}
        for id, color in self.COLOR_DEFS.items():
            prov_type = 'habitable'
            if id in self.SEA_PROVS: prov_type = 'sea'
            if id in self.RNW_PROVS: prov_type = 'RNW'
            if id in self.LAKE_PROVS: prov_type = 'lake'
            try:
                name = self.PROV_NAMES['PROV'+str(id)]
            except KeyError:
                name = undefined
                if prov_type not in ['RNW', 'lake']:
                    Log.warn('Province '+str(id)+' has no name')
            try: area = self._find_sub(self.ASSIGNMENT[0], id)
            except KeyError:
                area = undefined
                prov_type = 'wasteland'
            try: regn = self._find_sub(self.ASSIGNMENT[1], area)
            except KeyError: regn = undefined
            try: segn = self._find_sub(self.ASSIGNMENT[2], regn)
            except KeyError: segn = undefined
            prov = Province(self, name, prov_type, id)
            prov.set_color(color)
            prov.assign(area, regn, segn)
            try:
                prov.set_pixels(self.ID_POS[id])
                provinces[id] = prov
            except KeyError: pass
        self.provs = provinces


    def _load_map_def(self):
        path = self.CORE['path']['map-def']
        map_def = File(self, path, 'game', True)
        map_def = map_def.read()

        map_size = int(map_def['width'][0]), int(map_def['height'][0])
        sea_provs = [int(el) for el in map_def['sea_starts'][0]]
        rnw_provs = [int(el) for el in map_def['only_used_for_random'][0]]
        lake_provs = [int(el) for el in map_def['lakes'][0]]
        return map_size, sea_provs, rnw_provs, lake_provs

    def _load_clr_def(self):
        path = self.CORE['path']['color-def']
        clr_def = File(self, path, 'csv', True)
        clr_def = clr_def.read()
        clr_def = {int(row[0]):tuple([ int(el) for el in row[1:4] ])\
            for row in clr_def[1:]}
        return clr_def

    def _map_pixels_clr(self, img):
        id_from_clr = {v:k for k,v in self.COLOR_DEFS.items()}
        pixels = img.load()
        width, height = img.size
        result = {}
        for y in range(height):
            for x in range(width):
                px = pixels[x, y]
                try: result[id_from_clr[px]].append((x,y))
                except KeyError:
                    try: result[id_from_clr[px]] = [(x,y)]
                    except KeyError: pass
        return result

    def _prov_map_filter(self, image):
        pixels = image.load()
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x,y]
                r = (r+100)//4
                g = (g+100)//4
                b = (b+100)//4
                pixels[x, y] = (r,g,b)
        return image

    def _load_prov_map(self):
        path = self.CORE['path']['prov-map']
        prov_map = File(self, path, 'img', True)
        image = prov_map.read()
        id_pos = self._map_pixels_clr(image)
        self.SRC_IMG = image.copy()
        image = self._prov_map_filter(image)
        return id_pos, image

    def _load_localisation(self):
        path = self.CORE['path']['prov-names']
        locl = File(self, path, 'yaml', True)
        return locl.read()['l_'+self.LANG]

    def _load_assignment(self):
        path_area = self.CORE['path']['area-assign']
        path_regn = self.CORE['path']['regn-assign']
        path_segn = self.CORE['path']['segn-assign']
        areas = File(self, path_area, 'asgn', True).read()
        regns = File(self, path_regn, 'asgn', True).read()
        segns = File(self, path_segn, 'asgn', True).read()
        return areas, regns, segns

    def _find_sub(self, source, subject):
        for k, l in source.items():
            if subject in l:
                return k
        raise KeyError('Could not find "'+str(subject)+'" in the dict')

    def _get_id(self, fn):
        id = ''
        for c in fn:
            if c not in [str(d) for d in range(10)]:
                break
            id += c
        return int(id)
