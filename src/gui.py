'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
import wx
import wx.lib.scrolledpanel as scrl
from PIL import Image

from datetime import datetime # TEMP

import src.elems as el
from src.prov_group import ProvGroup

import logging
Log = logging.getLogger('MainLogger')

class MainFrame(wx.Frame):
    '''Defines Editor's GUI'''
    def __init__(self, core, locl):
        self.CORE, self.LOCL = core, locl
        el.init(self.CORE, self.LOCL)
        super().__init__(None, title=self.LOCL['frame-title'])

    def init_gui(self):
        img_panel_actions = {
            'lclick': self.on_map_lclick,
        }
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer()
        self.sizer.Add(self.side_bar(), pos=(0,1))

        bm = self.img_to_bm(self.MAP)
        self.img_panel = ImagePanel(self.panel, self.CORE, bm,
            img_panel_actions)
        self.sizer.Add(self.img_panel, pos=(0,0), flag=wx.EXPAND)

        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.panel.SetSizerAndFit(self.sizer)
        disp = wx.DisplaySize()
        self.SetSize(
            max([int(self.CORE['frame-x']*disp[0]), self.GetSize()[0]]),
            max([int(self.CORE['frame-y']*disp[1]), self.GetSize()[1]]),
        )

    def side_bar(self):
        sizer = wx.GridBagSizer()
        rows = [
            ('TEXT', 'lbl-view'),
            (self.on_zoom_in, 'scale-inc'),
            (self.on_zoom_out, 'scale-dec'),
            (self.on_zoom_reset, 'scale-rst'),
            ('TEXT', 'lbl-mapmodes'),
            (self.mapmode_provs, 'mm-provs'),
            (self.mapmode_areas, 'mm-areas'),
            (self.mapmode_regns, 'mm-regns'),
            (self.mapmode_segns, 'mm-segns'),
            (self.mapmode_custom, 'mm-cust'),
            ('TEXT', 'lbl-selection'),
            (self.on_unmark_all, 'unmark'),
        ]
        row = 0
        for action, key in rows:
            if action == 'TEXT':
                label = wx.StaticText(self.panel, label=self.LOCL[key],
                    style=wx.ALIGN_CENTRE_HORIZONTAL)
                sizer.Add(label, pos=(row,0), flag=wx.EXPAND)
            else:
                button = el.Button(self.panel, key, action)
                sizer.Add(button, pos=(row,0))
            row += 1
        return sizer

    def set_busy_on(self, event=None, key='msg-loading'):
        Log.info('Busy status started')
        self.isBusy = True
        self.Disable()
        self.busyDlg = wx.BusyInfo(self.LOCL[key])

    def set_busy_off(self, event=None):
        Log.info('Busy status ended')
        self.isBusy = False
        self.Enable()
        self.busyDlg = None

    # Map interactions

    def img_to_bm(self, image):
        width, height = image.size
        bm = wx.Bitmap.FromBuffer(width, height, image.tobytes())
        if self.SCALE != 1:
            image = bm.ConvertToImage()
            width, height = int(width*self.SCALE), int(height*self.SCALE)
            image = image.Scale(width, height)
            bm = image.ConvertToBitmap()
        return bm

    def mark_chunk(self, pxlist, color):
        '''Mark currently loaded map (self.MAP)'''
        pixels = self.MAP.load()
        for x, y in pxlist:
            pixels[x, y] = color
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def mark_src_map(self, pxlist, color):
        '''Mark source map (self.PROV_MAP)'''
        pixels = self.PROV_MAP.load()
        for x, y in pxlist:
            pixels[x, y] = color

    def on_map_lclick(self, event):
        x, y = event.GetPosition()
        scale = self.SCALE
        id = self._find_sub(self.chunk_pos, (int(x/scale),int(y/scale)))
        self.chunks[id].mark()

    def on_unmark_all(self, event):
        for id, chunk in self.chunks.items():
            if chunk.marked:
                self.chunks[id].mark()

    # Zoom methods

    def on_zoom_in(self, event):
        limit = self.CORE['scale-max']
        self.SCALE *= self.CORE['scale-step']
        if self.SCALE > limit:
            self.SCALE = limit
        if abs(1-self.SCALE) < self.CORE['scale-ignore']:
            self.SCALE = 1
        Log.info('Zoom in ('+str(round(self.SCALE, 3))+')')
        bm = self.img_to_bm(self.MAP)
        self.img_panel.load_bm(bm)

    def on_zoom_out(self, event):
        limit = self.CORE['scale-min']
        self.SCALE /= self.CORE['scale-step']
        if self.SCALE < limit:
            self.SCALE = limit
        if abs(1-self.SCALE) < self.CORE['scale-ignore']:
            self.SCALE = 1
        Log.info('Zoom out ('+str(round(self.SCALE, 3))+')')
        bm = self.img_to_bm(self.MAP)
        self.img_panel.load_bm(bm)

    def on_zoom_reset(self, event):
        Log.info('Zoom reset')
        self.SCALE = 1
        bm = self.img_to_bm(self.MAP)
        self.img_panel.load_bm(bm)

    # Map mode methods

    def mapmode_provs(self, event=None):
        self.MAPMODE = 'provs'
        self.MAP = self.PROV_MAP
        self.chunks = self.provs
        self.chunk_pos = {name:chunk.pixels
            for name, chunk in self.chunks.items()}
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def mapmode_areas(self, event):
        self.MAPMODE = 'areas'
        self._generate_map()
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def mapmode_regns(self, event):
        self.MAPMODE = 'regns'
        self._generate_map()
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def mapmode_segns(self, event):
        self.MAPMODE = 'segns'
        self._generate_map()
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def mapmode_custom(self, event):
        choices = list(self.CORE['spc-fkeys'].values())
        choices += list(self.CORE['num-fkeys'].values())
        choices += [el+' buildings' for el in self.CORE['bld-fkeys'].keys()]
        dialog = wx.SingleChoiceDialog(self, self.LOCL['dlg-mapmode-msg'],
            self.LOCL['dlg-mapmode-cpt'], choices)
        if dialog.ShowModal() == wx.ID_OK:
            self.MAPMODE = dialog.GetStringSelection()
        else: return
        self._generate_map()
        self.img_panel.load_bm(self.img_to_bm(self.MAP))

    def _generate_map(self):
        Log.info('Creating mapmode image')
        self.set_busy_on(key='msg-loading-map')
        time_a = datetime.now()
        groups = {}
        provinces = {}
        mapmode = self.MAPMODE
        for id, prov in self.provs.items():
            if mapmode == 'areas':
                group = prov.area
            elif mapmode == 'regns':
                group = prov.regn
            elif mapmode == 'segns':
                group = prov.segn
            else:
                try: group = prov.history[mapmode]
                except: continue
            try: groups[group].add_member(prov)
            except KeyError:
                groups[group] = ProvGroup(self, group, prov.type)
                groups[group].add_member(prov)
            provinces[id] = group
        for id, group in groups.items():
            group.set_color(group.calc_avg_color())
            group.get_mem_pixels()
        prov_pixels = self.SRC_IMG.load()
        image = Image.new('RGB', self.MAP_SIZE)
        group_pixels = image.load()
        reverse = {v:k for k,v in self.COLOR_DEFS.items()}
        width, height = self.MAP_SIZE
        for y in range(height):
            for x in range(width):
                prov_id = reverse[prov_pixels[x,y]]
                try: group_pixels[x,y] = groups[provinces[prov_id]].g_clr
                except KeyError: group_pixels[x,y] = (0,0,0)
        time_b = datetime.now()
        Log.info('Mapmode gen duration: '+str(time_b-time_a))
        self.chunks = groups
        self.chunk_pos = {name:chunk.pixels
            for name, chunk in self.chunks.items()}
        self.MAP = image
        for id, group in self.chunks.items():
            marked_count = sum(1 for prov in group.members if prov.marked)
            if marked_count >= len(group.members)*self.CORE['mark-group-perc']:
                group.mark()
            else:
                group.mark_members(force=False)
        self.set_busy_off()




class ImagePanel(scrl.ScrolledPanel):
    '''Scrolled Panel for Image'''
    def __init__(self, parent, config, bitmap, actions):
        super().__init__(parent)
        self.SetBackgroundColour((25,25,25))
        self.actions = actions
        self.CORE = config
        step = self.CORE['scroll-step']
        self.scroll = tuple([i/(100*step) for i in self.CORE['scroll-start']])

        self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.save_scroll_pos)
        self.img_sizer = wx.BoxSizer(wx.VERTICAL)
        self._load_bitmap(bitmap)
        self.SetSizer(self.img_sizer)
        self.move_scroll(self.scroll)

    def _load_bitmap(self, bitmap):
        self.st_bitmap = wx.StaticBitmap(self, bitmap=bitmap)
        self.st_bitmap.Bind(wx.EVT_LEFT_DOWN, self.actions['lclick'])
        self.img_sizer.Add(self.st_bitmap,1, wx.EXPAND)
        self.new_scroll(bitmap.GetSize())

    def load_bm(self, bitmap):
        self.st_bitmap.Destroy()
        self.move_scroll((0,0))
        self._load_bitmap(bitmap)
        self.move_scroll(self.scroll)

    def new_scroll(self, size):
        x, y = size
        self.size = size
        step = self.CORE['scroll-step']
        self.SetScrollbars(step, step, x//step, y//step)

    def move_scroll(self, percentage):
        x, y = percentage
        step = self.CORE['scroll-step']
        x = int(x*self.size[0])
        y = int(y*self.size[1])
        self.Scroll(x,y)

    def save_scroll_pos(self, event):
        scroll = self.scroll
        if event.Orientation == wx.HORIZONTAL:
            scroll = (event.GetPosition()/self.size[0], scroll[1])
        if event.Orientation == wx.VERTICAL:
            scroll = (scroll[0], event.GetPosition()/self.size[1])
        self.scroll = scroll
        event.Skip()
