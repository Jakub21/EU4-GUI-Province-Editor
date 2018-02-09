################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
import pandas as pd
from os import getcwd
import src.elems as el
from src.conf_parser import getWildcard
import time

################################
class frameDialog(wx.Frame):
    def __init__(self, _stt, _lang, _conf):
        self.InitSessionBegin = int(round(time.time() * 1000))
        self.sessionInitialized = False
        global lang
        lang = _lang
        global static
        static = _stt
        global conf
        conf = _conf
        super().__init__(None, title=lang['frame-title'])
        self.statusBusyStart()
        el.init(static, lang, conf)
        self.cwd = getcwd()

    ################
    # Disables whole Frame and shows dialog with no buttons
    def statusBusyStart(self, event=None):
        self.Disable()
        self.busyDlg = wx.BusyInfo(lang['startup_message'])

    def statusBusyEnd(self, event=None):
        self.Enable()
        self.busyDlg = None

    ################
    # Shows dialog with message (only OK as response)
    def prompt(self, dtype, key, data=''):
        flags = {
            'error'     : wx.OK|wx.ICON_ERROR,
            'warning'   : wx.OK|wx.ICON_EXCLAMATION,
            'info'      : wx.OK|wx.ICON_INFORMATION,
        }
        if (dtype not in flags):
            print('SCRIPT ERR', 'Unknown Dialog Type', sep='\n')
            exit()
        try:
            msg = lang['msg'][key]
        except KeyError:
            print('SCRIPT ERR', 'Unknown Dialog Message Key', sep='\n')
            exit()
        try:
            if len(str(data)) > 0:
                msg += '\n' + str(data)
        except:
            print('SCRIPT ERR',
                'Unhandled error occured while tried to add Data Info to Prompt',
                sep='\n'
            )
            raise
        dlg = wx.MessageDialog(None,
            message=msg,
            caption=lang['dlg'][dtype],
            style=flags[dtype]
        )
        dlg.ShowModal()
        dlg.Destroy()

################################
class ProgressDialog(wx.ProgressDialog):
    def __init__(self, tkey, mkey, dr, maximum, parent=None, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE):
        title = lang['dlg']['prg'][tkey]
        message = lang['dlg']['prg'][mkey] + dr
        super().__init__(title, message, maximum, parent, style)

################################
class FileDialog(wx.FileDialog):
    def __init__(self, message, wildcard):
        if type(wildcard) == str:
            wildcard = [wildcard]
        super().__init__(None, message=message, defaultDir=getcwd(), defaultFile='', wildcard=getWildcard(wildcard), style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

################################
class InitDialog(wx.Dialog):
    def __init__(self, static, lang):
        super().__init__(None, title=lang['init']['title'])
        self.SetSize(
            self.GetSize()[0] + static['init']['size-x'],
            self.GetSize()[1] + static['init']['size-y'],
        )
        if static['center_onscreen']:
            self.Center()
        self.initPanel()
    ################
    def initPanel(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer()
        self.pathstr = {}
        ################
        def selectFile(key):
            d = FileDialog(lang['init'][key], static['formats'][key])
            if d.ShowModal() == wx.ID_OK:
                path = d.GetPaths()[0]
                self.pathstr[key].Clear()
                self.pathstr[key].AppendText(path)
            else:
                pass
            d.Destroy()
        ################
        def addRow(key, row):
            def _action(event):
                selectFile(key)
            sizer.Add(wx.StaticText(panel, label=lang['init'][key]), flag=wx.EXPAND, pos=(row,0))
            self.pathstr[key] = el.TextCtrl(panel, conf['path'][key])
            sizer.Add(self.pathstr[key], flag=wx.EXPAND, pos=(row+1,0))
            button = el.Button(panel, label=lang['mb']['browse'])
            button.Bind(wx.EVT_BUTTON, _action)
            sizer.Add(button, pos=(row+1,1))
        ################
        addRow('area', 1)
        addRow('regn', 3)
        addRow('segn', 5)
        addRow('locl', 7)
        ################
        bSizer = wx.GridBagSizer()
        ################
        done = el.Button(panel, id=wx.ID_OK, label=lang['mb']['done'])
        bSizer.Add(done, pos=(0,0))
        ################
        cncl = el.Button(panel, id=wx.ID_CANCEL, label=lang['mb']['cancel'])
        cncl.SetFocus()
        bSizer.Add(cncl, pos=(0,1))
        ################
        sizer.Add(bSizer, pos=(9,0))
        panel.SetSizerAndFit(sizer)
