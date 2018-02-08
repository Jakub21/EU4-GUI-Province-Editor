################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
from src.conf_parser import getlcl, getstatic, getconf
from src.menu import frameMenu
import wx

################################
class mainFrame(frameMenu):
    def __init__(self):
        global static
        static = getstatic()
        global lang
        lang = getlcl()
        global conf
        conf = getconf()
        super().__init__(static, lang, conf)
        self.initPanel()
        self.initStatusBar()
        if static['center_onscreen']:
            self.Center()
        self.SetSize(
            self.GetSize()[0] + static['frame-x'],
            self.GetSize()[1] + static['frame-y']
        )
        self.statusBusyEnd()
        self.Show()

    def initStatusBar(self):
        self.CreateStatusBar()
        self.SetStatusText(lang['st']['home'])

    def initPanel(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer()

        btt = wx.Button(self.panel, label=lang['mb']['set-title'],
            size=(static['cell-x'], static['cell-y']))
        self.Bind(wx.EVT_BUTTON, self.action, btt)
        self.sizer.Add(btt, pos=(1,1))

        btt = wx.Button(self.panel, label=lang['mb']['inpr-title'],
            size=(static['cell-x'], static['cell-y']))
        self.Bind(wx.EVT_BUTTON, self.action, btt)
        self.sizer.Add(btt, pos=(2,1))

        for i in static['mf']['grw-col']:
            self.sizer.AddGrowableCol(i)
        for i in static['mf']['grw-row']:
            self.sizer.AddGrowableRow(i)
        self.panel.SetSizerAndFit(self.sizer)
