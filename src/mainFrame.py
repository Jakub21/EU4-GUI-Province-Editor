################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
from src.conf_parser import getlcl, getstatic, getconf
import src.elems as el
from src.menu import frameMenu
import wx
import time

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
        if static['center-on-screen']:
            self.Center()
        self.SetSize(
            self.GetSize()[0] + static['frame-x'],
            self.GetSize()[1] + static['frame-y']
        )
        self.statusBusyEnd()
        self.InitSessionEnd = int(round(time.time() * 1000))
        self.Show()

    def initStatusBar(self):
        self.CreateStatusBar()
        self.SetStatusText(lang['st']['home'])

    def initPanel(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer()
        ################
        # Text Repr. of Data
        FONT = wx.Font(conf['repr-font-size'],
            wx.MODERN, wx.NORMAL, wx.NORMAL,
            False, 'Consolas'
        )
        self.outText = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.sizer.Add(self.outText, pos=(0,0), flag=wx.EXPAND)
        self.outText.SetFont(FONT)
        ################
        # Right side sizer
        self.bSizer = wx.GridBagSizer()
        btt = el.Button(self.panel,'set-title', self.action)
        self.bSizer.Add(btt, pos=(0,0))

        btt = el.Button(self.panel,'inpr-title', self.action)
        self.bSizer.Add(btt, pos=(1,0))

        btt = el.Button(self.panel,'cmd-title', self.action)
        self.bSizer.Add(btt, pos=(2,0))

        self.sizer.Add(self.bSizer, pos=(0,1), span=(1,1))
        btt.SetFocus()
        ################

        for i in static['mf']['grw-col']:
            self.sizer.AddGrowableCol(i)
        for i in static['mf']['grw-row']:
            self.sizer.AddGrowableRow(i)
        self.panel.SetSizerAndFit(self.sizer)
