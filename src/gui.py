'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
import wx
import wx.lib.scrolledpanel as scrl
import src.elems as el

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

        bm = self.img_to_bm(self.PROV_MAP)
        self.img_panel = ImagePanel(self.panel, self.CORE, bm, img_panel_actions)
        self.sizer.Add(self.img_panel, pos=(0,0), flag=wx.EXPAND)

        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.panel.SetSizerAndFit(self.sizer)

    def side_bar(self):
        sizer = wx.GridBagSizer()
        buttons_data = [
            (0, self.on_zoom_in, 'scale-inc'),
            (1, self.on_zoom_out, 'scale-dec'),
            (2, self.on_zoom_reset, 'scale-rst'),
            (3, self.on_unmark_all, 'unmark'),
        ]
        for row, action, key in buttons_data:
            button = el.Button(self.panel, key, action)
            sizer.Add(button, pos=(row,0))
        return sizer

    def set_busy_on(self, event=None):
        Log.info('Busy status started')
        self.isBusy = True
        self.Disable()
        self.busyDlg = wx.BusyInfo(self.LOCL['msg-loading'])

    def set_busy_off(self, event=None):
        Log.info('Busy status ended')
        self.isBusy = False
        self.Enable()
        self.busyDlg = None

    def img_to_bm(self, image):
        width, height = image.size
        bm = wx.Bitmap.FromBuffer(width, height, image.tobytes())
        if self.SCALE != 1:
            image = bm.ConvertToImage()
            width, height = int(width*self.SCALE), int(height*self.SCALE)
            image.Rescale(width, height, wx.IMAGE_QUALITY_BICUBIC)
            bm = image.ConvertToBitmap()
        return bm

    def mark_prov_map(self, pxlist, color):
        pixels = self.PROV_MAP.load()
        for x, y in pxlist:
            pixels[x, y] = color
        self.img_panel.load_bm(self.img_to_bm(self.PROV_MAP))

    def on_map_lclick(self, event):
        x, y = event.GetPosition()
        id = self._find_sub(self.ID_POS, (int(x/self.SCALE),int(y/self.SCALE)))
        self.provs[id].mark()

    def on_unmark_all(self, event):
        for id, prov in self.provs.items():
            if prov.marked:
                self.provs[id].mark()

    def on_zoom_in(self, event):
        limit = self.CORE['scale-max']
        self.SCALE *= self.CORE['scale-step']
        if self.SCALE > limit:
            self.SCALE = limit
        if abs(1-self.SCALE) < self.CORE['scale-ignore']:
            self.SCALE = 1
        Log.info('Zoom in ('+str(round(self.SCALE, 3))+')')
        bm = self.img_to_bm(self.PROV_MAP)
        self.img_panel.load_bm(bm)

    def on_zoom_out(self, event):
        limit = self.CORE['scale-min']
        self.SCALE /= self.CORE['scale-step']
        if self.SCALE < limit:
            self.SCALE = limit
        if abs(1-self.SCALE) < self.CORE['scale-ignore']:
            self.SCALE = 1
        Log.info('Zoom out ('+str(round(self.SCALE, 3))+')')
        bm = self.img_to_bm(self.PROV_MAP)
        self.img_panel.load_bm(bm)

    def on_zoom_reset(self, event):
        Log.info('Zoom reset')
        self.SCALE = 1
        bm = self.img_to_bm(self.PROV_MAP)
        self.img_panel.load_bm(bm)




class ImagePanel(scrl.ScrolledPanel):
    '''Scrolled Panel for Image'''
    def __init__(self, parent, config, bitmap, actions):
        super().__init__(parent)
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
