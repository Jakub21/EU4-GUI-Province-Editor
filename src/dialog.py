################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
# TODO: Check if there are unnecessary imports
import wx
import pandas as pd
from os import getcwd
import src.elems as el
from src.conf_parser import getWildcard
from datetime import datetime
from wx.lib.masked.numctrl import NumCtrl as NumCtrl
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class frameDialog(wx.Frame):
    def __init__(self, _stt, _lang, _conf):
        self.InitSessionBegin = datetime.now()
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
        Log.info('Busy Status Started')
        self.Disable()
        self.busyDlg = wx.BusyInfo(lang['startup-message'])

    def statusBusyEnd(self, event=None):
        Log.info('Busy Status Finished')
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
            Log.info('Unknown Dialog Type')
        try:
            msg = lang['msg'][key]
        except KeyError:
            Log.info('Unknown Dialog Message Key')
            raise
        try:
            if len(str(data)) > 0:
                msg += '\n' + str(data)
        except:
            Log.info('Unhandled error occurred while tried to add Data Info to Prompt')
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
    def __init__(self, tKey, mKey, detail='', maximum=100, parent=None,
        style=wx.PD_CAN_ABORT|wx.PD_APP_MODAL|wx.PD_AUTO_HIDE):
        self.parent = parent
        if self.parent != None:
            self.parent.Disable()
        title = lang['dlg']['prg'][tKey]
        message = lang['dlg']['prg'][mKey]+'\n'+detail
        super().__init__(title, message, maximum, parent, style)

    def Update(self, amount, mKey, detail):
        return super().Update(amount, lang['dlg']['prg'][mKey]+'\n'+detail)

    def Destroy(self):
        if self.parent != None:
            self.parent.Enable()
        super().Destroy()

################################
class FileDialog(wx.FileDialog):
    def __init__(self, message, wildcard, mode, default=''):
        if mode == 'open':
            style = wx.FD_OPEN
        elif mode == 'save':
            style = wx.FD_SAVE
        style += wx.FD_CHANGE_DIR
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
# Following dialogs inherit from this one
class basicDialog(wx.Dialog):
    def __init__(self, title, style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
        super().__init__(None, title=title, style=style)

################################
class SelectDialog(basicDialog):
    def __init__(self, mode, src):
        super().__init__(lang['dlg'][mode])
        self.initPanel()
        self.SetSize(
            self.GetSize()[0] + 20,
            self.GetSize()[1] + 40,
        )
        if static['center-on-screen']:
            self.Center()
        self.SRC = src

    def initPanel(self):
        ################################
        def updateAttrlist(event):
            i = self.ListCol.GetString(self.ListCol.GetSelection())
            self.AttrList.Set(list(set(self.SRC[i])))
        ################################
        choices = [
            i for i in static['column-order'] if i not in set(conf['rem-from-repr'])
        ]
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer()

        self.ListCol = wx.ListBox(self.panel, choices=choices)
        self.ListCol.Bind(wx.EVT_LISTBOX, updateAttrlist)
        sizer.Add(self.ListCol, pos=(0,0), flag=wx.EXPAND)

        self.AttrList = wx.CheckListBox(self.panel,
            style=wx.LB_SORT|wx.LB_NEEDED_SB|wx.LB_MULTIPLE)
        sizer.Add(self.AttrList, pos=(0,1), flag=wx.EXPAND)
        ################
        bSizer = wx.GridBagSizer()
        done = el.Button(self.panel, 'done', id=wx.ID_OK)
        bSizer.Add(done, pos=(0,0))
        cncl = el.Button(self.panel, 'cancel', id=wx.ID_CANCEL)
        cncl.SetFocus()
        bSizer.Add(cncl, pos=(0,1))
        sizer.Add(bSizer, pos=(1,0))
        ################
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        self.panel.SetSizer(sizer)

################################
class ModifyDialog(basicDialog):
    def __init__(self, mode, src):
        super().__init__(lang['dlg'][mode])
        self.SRC = src
        self.MODE = mode
        self.initPanel()
        self.SetSize(
            self.GetSize()[0] + 20,
            self.GetSize()[1] + 40,
        )
        if static['center-on-screen']:
            self.Center()

    def initPanel(self):
        ################################
        def updateAttrlist(event):
            L = self.ListCol.GetString(self.ListCol.GetSelection())
            L = sorted(list(set(map(lambda x: str(x), self.SRC[L]))))
            self.AttrList.Set([lang['other']]+L)
            self.AttrList.SetSelection(0)
        def checkOther(event):
            if self.AttrList.GetSelection() == 0:
                self.OtherName.Enable()
            else:
                self.OtherName.Disable()
        ################################
        choices = [
            i for i in static['column-order'] if i not in set(conf['rem-from-repr'])
        ]
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer()

        self.ListCol = wx.ListBox(self.panel, choices=choices)
        self.ListCol.Bind(wx.EVT_LISTBOX, updateAttrlist)
        sizer.Add(self.ListCol, pos=(0,0), span=(0,1), flag=wx.EXPAND)

        self.AttrList = wx.ListBox(self.panel,
            style=wx.LB_NEEDED_SB)
        self.AttrList.Bind(wx.EVT_LISTBOX, checkOther)
        sizer.Add(self.AttrList, pos=(0,1), flag=wx.EXPAND)
        try:
            self.AttrList.SetSelection(0)
        except wx._core.wxAssertionError: pass

        x = 0
        if self.MODE == 'modify-prov':
            sizer.Add(wx.StaticText(self.panel, label=lang['dlg']['mod-prov-inp']),
                pos=(1,0), flag=wx.EXPAND)
            self.ProvInput = el.TextCtrl(self.panel, '')
            sizer.Add(self.ProvInput, pos=(1,1), flag=wx.EXPAND)
            x = 1

        sizer.Add(wx.StaticText(self.panel, label=lang['dlg']['mod-oth-inp']),
            pos=(x+1,0), flag=wx.EXPAND)

        self.OtherName = el.TextCtrl(self.panel, '')
        sizer.Add(self.OtherName, pos=(x+1,1), flag=wx.EXPAND)
        ################
        bSizer = wx.GridBagSizer()
        done = el.Button(self.panel, 'done', id=wx.ID_OK)
        done.SetFocus()
        bSizer.Add(done, pos=(0,0))
        cncl = el.Button(self.panel, 'cancel', id=wx.ID_CANCEL)
        bSizer.Add(cncl, pos=(0,1))
        sizer.Add(bSizer, pos=(x+2,0))
        ################
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        self.panel.SetSizer(sizer)

################################
class ConfigDialog(basicDialog):
    def __init__(self):
        super().__init__(lang['CONF']['title'])
        self.initPanel()
        self.SetSize(
            self.GetSize()[0] + 150,
            self.GetSize()[1] + 290,
        )
        if static['center-on-screen']:
            self.Center()

    def initPanel(self):
        self.PathStr = {}
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer()
        pathSizer = wx.GridBagSizer()
        ################################
        # Repr Font Size
        sizer.Add(wx.StaticText(self.panel, label=lang['CONF']['font']),
            flag=wx.EXPAND, pos=(9,0))
        self.fontSize = NumCtrl(self.panel, value=conf['repr-font-size'])
        sizer.Add(self.fontSize, pos=(10,0))#, flag=wx.EXPAND)
        ################################
        # Hide no-segion provinces
        sizer.Add(wx.StaticText(self.panel, label=lang['CONF']['no-segn']),
            flag=wx.EXPAND, pos=(11,0))
        self.NoSegn = wx.CheckBox(self.panel)
        self.NoSegn.SetValue(conf['hide-no-segn'])
        sizer.Add(self.NoSegn, pos=(12,0), flag=wx.EXPAND)
        ################################
        # Attribute Files
        def selectFile(key):
            d = FileDialog(lang['CONF'][key], static['formats'][key], 'open',
                static['names'][key]+'.'+static['formats'][key])
            if d.ShowModal() == wx.ID_OK:
                path = d.GetPaths()[0]
                self.PathStr[key].Clear()
                self.PathStr[key].AppendText(path)
            d.Destroy()
        def addRow(key, row):
            def Action(event):
                selectFile(key)
            sizer.Add(wx.StaticText(self.panel, label=lang['CONF'][key]),
                flag=wx.EXPAND, pos=(row,0))
            self.PathStr[key] = el.TextCtrl(self.panel, conf['path'][key])
            sizer.Add(self.PathStr[key], flag=wx.EXPAND, pos=(row+1,0))
            button = el.Button(self.panel, 'browse', Action)
            sizer.Add(button, pos=(row+1,1))
        addRow('area', 1)
        addRow('regn', 3)
        addRow('segn', 5)
        addRow('locl', 7)
        sizer.Add(pathSizer, pos=(0,0), span=(0,1), flag=wx.EXPAND)
        ################################
        # Hidden Columns
        sizer.Add(wx.StaticText(self.panel, label=lang['CONF']['hidden']),
            flag=wx.EXPAND, pos=(13,0))
        self.hiddenCols = wx.CheckListBox(self.panel,
            style=wx.LB_NEEDED_SB|wx.LB_MULTIPLE)
        self.hiddenCols.Set(static['column-order'])
        self.hiddenCols.SetCheckedStrings(conf['rem-from-repr'])
        sizer.Add(self.hiddenCols, pos=(14,0), flag=wx.EXPAND)
        ################################
        # Bottom buttons
        bSizer = wx.GridBagSizer()
        done = el.Button(self.panel, 'done', id=wx.ID_OK)
        bSizer.Add(done, pos=(0,0))
        cncl = el.Button(self.panel, 'cancel', id=wx.ID_CANCEL)
        cncl.SetFocus()
        bSizer.Add(cncl, pos=(0,1))
        sizer.Add(bSizer, pos=(15,0), flag=wx.EXPAND)
        ################################
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(14)
        self.panel.SetSizerAndFit(sizer)
