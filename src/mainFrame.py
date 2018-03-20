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
from datetime import datetime
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class mainFrame(frameMenu):
    def __init__(self, isDebug):
        global static
        static = getstatic()
        global lang
        lang = getlcl()
        global conf
        conf = getconf()
        super().__init__(static, lang, conf)
        self.isDebug = isDebug
        Log.info('Initializing GUI')
        self.initPanel()
        self.initStatusBar()
        self.SetSize(
            self.GetSize()[0] + 180,
            self.GetSize()[1] + 150,
        )
        self.statusBusyEnd()
        self.InitSessionEnd = datetime.now()
        if static['center-on-screen']:
            self.Center()
        Log.info('Revealing Frame')
        self.Show()

    def initStatusBar(self):
        self.CreateStatusBar()
        self.SetStatusText(lang['st']['home'])

    def initPanel(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer()
        ################
        # Text Repr. of Data
        self.outText = wx.TextCtrl(self.panel, value=lang['repr']+'\n',
            style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.sizer.Add(self.outText, pos=(0,0),  flag=wx.EXPAND)
        # Changing font
        FontSize = conf['repr-font-size']
        Log.info('Changing font of Repr to '+str(FontSize)+' px')
        FONT = wx.Font(FontSize, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Consolas')
        self.outText.SetFont(FONT)
        ################
        # Right side sizer
        self.bSizer = wx.GridBagSizer()
        btt = el.Button(self.panel,'mod-col-btt', self.actionModifyColumn)
        self.bSizer.Add(btt, pos=(0,0))

        btt = el.Button(self.panel,'mod-prov-btt', self.actionModifyProvince)
        self.bSizer.Add(btt, pos=(1,0))

        self.sizer.Add(self.bSizer, pos=(0,1), span=(1,1))
        btt.SetFocus()
        ################

        for i in [0]:
            self.sizer.AddGrowableCol(i)
        for i in [0]:
            self.sizer.AddGrowableRow(i)
        self.panel.SetSizerAndFit(self.sizer)
