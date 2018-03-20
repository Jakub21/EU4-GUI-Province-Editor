################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
from src.actions import frameActions
import wx
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class frameMenu(frameActions):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)
        Log.info('Initializing Menu Bar')
        self.initMenu()

    def initMenu(self):
        ################
        # MAIN MENU
        mmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.Configure,
            mmenu.Append(-1, lang['mb']['run-static-title'], lang['mb']['run-static-desc']))
        self.Bind(wx.EVT_MENU, self.actionQuit,
            mmenu.Append(-1, lang['mb']['quit-title'], lang['mb']['quit-desc']))

        ################
        # FILE MENU
        fmenu = wx.Menu()
        # Load
        self.Bind(wx.EVT_MENU, self.actionLoadSheet,
            fmenu.Append(-1, lang['mb']['load-s-title'], lang['mb']['load-s-desc']))
        self.Bind(wx.EVT_MENU, self.actionLoadOrig,
            fmenu.Append(-1, lang['mb']['load-g-title'], lang['mb']['load-g-desc']))
        # Load-update
        fmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.actionLoadUpdSheet,
            fmenu.Append(-1, lang['mb']['loadu-s-title'], lang['mb']['loadu-s-desc']))
        self.Bind(wx.EVT_MENU, self.actionLoadUpdOrig,
            fmenu.Append(-1, lang['mb']['loadu-g-title'], lang['mb']['loadu-g-desc']))
        # Save
        fmenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.actionSaveSheet,
            fmenu.Append(-1, lang['mb']['save-s-title'], lang['mb']['save-s-desc']))
        self.Bind(wx.EVT_MENU, self.actionSaveOrig,
            fmenu.Append(-1, lang['mb']['save-g-title'], lang['mb']['save-g-desc']))

        ################
        # SELECTION MENU
        smenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.actionSelectNew,
            smenu.Append(-1, lang['mb']['sel-new-title'], lang['mb']['sel-new-desc']))
        self.Bind(wx.EVT_MENU, self.actionSelectSub,
            smenu.Append(-1, lang['mb']['sel-sub-title'], lang['mb']['sel-sub-desc']))
        self.Bind(wx.EVT_MENU, self.actionSelectApp,
            smenu.Append(-1, lang['mb']['sel-app-title'], lang['mb']['sel-app-desc']))
        # Deselect
        smenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.action,
            smenu.Append(-1, lang['mb']['desel-t-title'], lang['mb']['desel-t-desc']))
        self.Bind(wx.EVT_MENU, self.action,
            smenu.Append(-1, lang['mb']['desel-n-title'], lang['mb']['desel-n-desc']))

        ################
        # SORT MENU
        rmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.actionSortByID,
            rmenu.Append(-1, lang['mb']['sort-id-title'], lang['mb']['sort-id-desc']))
        self.Bind(wx.EVT_MENU, self.actionSortByLoc,
            rmenu.Append(-1, lang['mb']['sort-loc-title'], lang['mb']['sort-loc-desc']))

        ################
        # MODIFY MENU
        qmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.actionModifyColumn,
            qmenu.Append(-1, lang['mb']['mod-col-title'], lang['mb']['mod-col-desc']))
        self.Bind(wx.EVT_MENU, self.actionModifyProvince,
            qmenu.Append(-1, lang['mb']['mod-prov-title'], lang['mb']['mod-prov-desc']))
        ################
        # MENU BAR
        menubar = wx.MenuBar()
        menubar.Append(mmenu, lang['menu']['main'])
        menubar.Append(fmenu, lang['menu']['file'])
        menubar.Append(smenu, lang['menu']['selc'])
        menubar.Append(rmenu, lang['menu']['sort'])
        menubar.Append(qmenu, lang['menu']['modf'])
        self.SetMenuBar(menubar)
