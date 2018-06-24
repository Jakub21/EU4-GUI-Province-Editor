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
        global CORE, LOCL
        CORE, LOCL = core, locl
        el.init(CORE, LOCL)
        super().__init__(None, title=LOCL['frame-title'])

    def init_gui(self):
        actions = [self.on_map_lclick]
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer()
        self.sizer.Add(self.side_bar(), pos=(0,1))
        provs_bm = self.img_to_bm(self.PROV_MAP)
        self.img_panel = ImagePanel(self.panel, provs_bm, actions)
        self.sizer.Add(self.img_panel, pos=(0,0), flag=wx.EXPAND)

        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        scroll_start = tuple(CORE['scroll-start'])
        self.img_panel.Scroll(scroll_start)
        self.panel.SetSizerAndFit(self.sizer)

    def side_bar(self):
        sizer = wx.GridBagSizer()
        label_keys = ['scale-inc', 'scale-dec', 'unmark']
        actions = [self.on_zoom_in, self.on_zoom_out, self.unmark_all]
        for lab, act, ind in zip(label_keys, actions, range(len(label_keys))):
            bttn = el.Button(self.panel, lab, act)
            sizer.Add(bttn, pos=(ind,0))
        return sizer

    def set_busy_on(self, event=None):
        Log.info('Busy status started')
        self.isBusy = True
        self.Disable()
        self.busyDlg = wx.BusyInfo(LOCL['msg-loading'])

    def set_busy_off(self, event=None):
        Log.info('Busy status ended')
        self.isBusy = False
        self.Enable()
        self.busyDlg = None

    def img_to_bm(self, image):
        width, height = image.size
        bm = wx.Bitmap.FromBuffer(width, height, image.tobytes())
        return bm

    def unmark_all(self, event):
        for id, prov in self.provs.items():
            if prov.marked:
                self.provs[id].mark()

    def on_map_lclick(self, event):
        x, y = event.GetPosition()
        id = self._find_sub(self.ID_POS, (int(x/self.SCALE),int(y/self.SCALE)))
        self.provs[id].mark()

    def _rescale(self, image):
        width, height = image.size
        bm = wx.Bitmap.FromBuffer(width, height, image.tobytes())
        image = bm.ConvertToImage()
        width, height = int(width*self.SCALE), int(height*self.SCALE)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bm = image.ConvertToBitmap()
        return bm

    def on_zoom_in(self, event):
        self.SCALE *= self.CORE['scale-step']
        Log.info('Rescaling image: '+str(self.SCALE))
        bm = self._rescale(self.PROV_MAP)
        self.img_panel.load_bm(bm)

    def on_zoom_out(self, event):
        self.SCALE /= self.CORE['scale-step']
        Log.info('Rescaling image: '+str(self.SCALE))
        bm = self._rescale(self.PROV_MAP)
        self.img_panel.load_bm(bm)

    def _update_map(self, pxlist, color):
        image = self.PROV_MAP
        pixels = image.load()
        for x,y in pxlist:
            pixels[x,y] = color
        self.PROV_MAP = image
        self.img_panel.load_bm(self.img_to_bm(image))


class ImagePanel(scrl.ScrolledPanel):
    '''Scrolled Panel for Image'''
    def __init__(self, parent, bitmap, actions):
        super().__init__(parent)
        self.actions = actions
        self.scroll = tuple(CORE['scroll-start'])
        self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.update_scroll)
        self.img_sizer = wx.BoxSizer(wx.VERTICAL)
        self.st_bitmap = wx.StaticBitmap(self, bitmap=bitmap)
        self.st_bitmap.Bind(wx.EVT_LEFT_DOWN, self.actions[0])
        self.img_sizer.Add(self.st_bitmap, 1, wx.EXPAND)
        self.SetSizer(self.img_sizer)
        self.set_scrl_bars(bitmap.GetSize())

    def load_bm(self, bitmap):
        self.st_bitmap.Destroy()
        self.Scroll(0,0)
        self.st_bitmap = wx.StaticBitmap(self, bitmap=bitmap)
        self.st_bitmap.Bind(wx.EVT_LEFT_DOWN, self.actions[0])
        self.img_sizer.Add(self.st_bitmap,1, wx.EXPAND)
        self.Scroll(self.scroll)
        self.set_scrl_bars(bitmap.GetSize())

    def set_scrl_bars(self, size):
        x, y = size
        sr = CORE['scroll-step']
        self.SetScrollbars(sr, sr, x//sr, y//sr)

    def update_scroll(self, event):
        scroll = self.scroll
        if event.Orientation == wx.HORIZONTAL:
            scroll = (event.GetPosition(), scroll[1])
        if event.Orientation == wx.VERTICAL:
            scroll = (scroll[0], event.GetPosition())
        self.scroll = scroll
        event.Skip()
