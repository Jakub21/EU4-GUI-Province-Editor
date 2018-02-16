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
        self.cwd = getcwd().replace('\\', '/') + '/'

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
    def __init__(self, tkey, mkey, detail, maximum, parent=None,
                style=wx.PD_CAN_ABORT|wx.PD_APP_MODAL|wx.PD_AUTO_HIDE
            ):
        self.parent = parent
        if self.parent!=None:
            self.parent.Disable()
        title = lang['dlg']['prg'][tkey]
        message = lang['dlg']['prg'][mkey]+'\n'+detail
        super().__init__(title, message, maximum, parent, style)

    def Update(self, amount, mkey, detail):
        return super().Update(amount, lang['dlg']['prg'][mkey]+'\n'+detail)

    def Destroy(self):
        if self.parent!=None:
            self.parent.Enable()
        super().Destroy()

    def Close(self):
        self.prompt('info', 'sure-exit')

################################
class FileDialog(wx.FileDialog):
    def __init__(self, message, wildcard, mode, default=''):
        if mode == 'open':
            style = wx.FD_OPEN | wx.FD_CHANGE_DIR
        elif mode == 'save':
            style = wx.FD_SAVE | wx.FD_CHANGE_DIR
        if type(wildcard) == str:
            wildcard = [wildcard]
        super().__init__(None,
            message=message,
            defaultDir=getcwd(),
            defaultFile=default,
            wildcard=getWildcard(wildcard),
            style=style
        )

################################
class SelectDialog(wx.Dialog):
    def __init__(self, mode, src):
        super().__init__(None, title=lang['dlg'][mode])
        if static['center-on-screen']:
            self.Center()
        self.initPanel()
        self.mode = mode
        self.SRC = src
    ################
    def initPanel(self):
        ################
        def updateAttrlist(event):
            i = self.col.GetString(self.col.GetSelection())
            self.attrList.Set(list(set(self.SRC[i])))
        ################
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer()

        self.col = wx.ListBox(self.panel, choices=conf['column-display'])
        self.col.Bind(wx.EVT_LISTBOX, updateAttrlist)
        sizer.Add(self.col, pos=(0,0), flag=wx.EXPAND)

        self.attrList = wx.CheckListBox(self.panel,
            style=wx.LB_SORT|wx.LB_NEEDED_SB|wx.LB_MULTIPLE)
        sizer.Add(self.attrList, pos=(0,1), flag=wx.EXPAND)


        done = el.Button(self.panel, 'done', id=wx.ID_OK)
        sizer.Add(done, pos=(1,0))
        cncl = el.Button(self.panel, 'cancel', id=wx.ID_CANCEL)
        sizer.Add(cncl, pos=(1,1))

        cncl.SetFocus()
        self.panel.SetSizer(sizer)


################################
class InitDialog(wx.Dialog):
    def __init__(self, static, lang):
        super().__init__(None, title=lang['init']['title'])
        self.SetSize(
            self.GetSize()[0] + static['init']['size-x'],
            self.GetSize()[1] + static['init']['size-y'],
        )
        if static['center-on-screen']:
            self.Center()
        self.initPanel()
    ################
    def initPanel(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer()
        self.pathstr = {}
        ################
        def selectFile(key):
            d = FileDialog(lang['init'][key],
                static['formats'][key],
                'open',
                static['names'][key] + '.' + static['formats'][key]
            )
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
            button = el.Button(panel, 'browse')
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
        done = el.Button(panel, 'done', id=wx.ID_OK)
        bSizer.Add(done, pos=(0,0))
        ################
        cncl = el.Button(panel, 'cancel', id=wx.ID_CANCEL)
        cncl.SetFocus()
        bSizer.Add(cncl, pos=(0,1))
        ################
        sizer.Add(bSizer, pos=(9,0))
        panel.SetSizerAndFit(sizer)
