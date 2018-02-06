################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
from src.actions import frameActions
import wx

################################
class frameMenu(frameActions):
    def __init__(self, _conf, _lang):
        global conf
        conf = _conf
        global lang
        lang = _lang
        super().__init__(conf, lang)
        self.initMenu()

    def initMenu(self):
        ################
        # FILE MENU
        fmenu = wx.Menu()
        # Load
        self.Bind(wx.EVT_MENU, self.action,
            fmenu.Append(-1, lang['mb']['load-s-title'], lang['mb']['load-s-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            fmenu.Append(-1, lang['mb']['load-g-title'], lang['mb']['load-g-desc']))
        # Save
        fmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.action,
            fmenu.Append(-1, lang['mb']['save-s-title'], lang['mb']['save-s-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            fmenu.Append(-1, lang['mb']['save-g-title'], lang['mb']['save-g-desc']))
        # Others
        fmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.actionQuit,
            fmenu.Append(-1, lang['mb']['quit-title'], lang['mb']['quit-desc']))

        ################
        # DATA MENU
        dmenu = wx.Menu()
        # Selection
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sel-new-title'], lang['mb']['sel-new-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sel-sub-title'], lang['mb']['sel-sub-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sel-app-title'], lang['mb']['sel-app-desc']))
        # Deselection
        dmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['desel-title'], lang['mb']['desel-desc']))
        # Sort
        dmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sort-id-title'], lang['mb']['sort-id-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sort-col-title'], lang['mb']['sort-col-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            dmenu.Append(-1, lang['mb']['sort-loc-title'], lang['mb']['sort-loc-desc']))
        ################
        # MENU BAR
        menubar = wx.MenuBar()
        menubar.Append(fmenu, lang['menu']['file'])
        menubar.Append(dmenu, lang['menu']['data'])
        self.SetMenuBar(menubar)
