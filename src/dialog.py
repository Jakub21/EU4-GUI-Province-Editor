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

################################
class frameDialog(wx.Frame):
    def __init__(self, _stt, _lang, _conf):
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
        self.busyDlg = wx.BusyInfo(lang['loading'])

    def statusBusyEnd(self, event=None):
        self.Enable()
        self.busyDlg = None

    ################
    # Shows dialog with message (only OK as response)
    def prompt(self, dtype, key, SelfMessage=False):
        flags = {
            'error'     : wx.OK|wx.ICON_ERROR,
            'warning'   : wx.OK|wx.ICON_EXCLAMATION,
            'info'      : wx.OK|wx.ICON_INFORMATION,
        }
        if (dtype not in flags) and not(SelfMessage):
            print('SCRIPT ERR', 'Unknows Dialog Type', sep='\n')
            exit(0)
        if SelfMessage:
            msg = key
        else:
            msg = lang['msg'][key]
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
        self.initPanel()

    ################
    #def apply(self, event):
    #    return wx.ID_OK
    #    self.Destroy()

    ################
    #def cancel(self, event):
    #    return wx.ID_CANCEL
    #    self.Destroy()

    ################
    def selectFile(self, mode):
        d = FileDialog(lang['init'][mode], static['formats'][mode])
        if d.ShowModal() == wx.ID_OK:
            path = d.GetPaths()[0]
        else:
            pass
        d.Destroy()


    ################
    # Probably there's a better way to do this
    # Binding button to func. with argument is required
    # TODO
    def selectArea(self, event):
        self.selectFile('area')
    def selectRegion(self, event):
        self.selectFile('region')
    def selectSegion(self, event):
        self.selectFile('segion')
    def selectLocl(self, event):
        self.selectFile('locl')
    ################

    ################
    def initPanel(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer()
        ################
        def addRow(key, row, action):
            sizer.Add(wx.StaticText(panel, label=lang['init'][key]), flag=wx.EXPAND, pos=(row,0))
            pathstr = el.TextCtrl(panel, id=row, conf['path'][key])
            sizer.Add(pathstr, flag=wx.EXPAND, pos=(row+1,0))
            button = el.Button(panel, label=lang['mb']['browse'])
            button.Bind(wx.EVT_BUTTON, action)
            sizer.Add(button, pos=(row+1,1))
        ################
        addRow('area',      1, self.selectArea)
        addRow('region',    3, self.selectRegion)
        addRow('segion',    5, self.selectSegion)
        addRow('locl',      7, self.selectLocl)
        ################
        bSizer = wx.GridBagSizer()
        ################
        done = el.Button(panel, id=wx.ID_OK, label=lang['mb']['done'])
        #done.Bind(wx.EVT_BUTTON, self.apply)
        bSizer.Add(done, pos=(0,0))
        ################
        cncl = el.Button(panel, id=wx.ID_CANCEL, label=lang['mb']['cancel'])
        #cncl.Bind(wx.EVT_BUTTON, self.cancel)
        cncl.SetFocus()
        bSizer.Add(cncl, pos=(0,1))
        ################
        sizer.Add(bSizer, pos=(9,0))
        panel.SetSizerAndFit(sizer)
