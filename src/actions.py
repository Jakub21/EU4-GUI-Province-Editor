################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
import pandas as pd
import src.dialog as dlg
from numpy import nan
from src.engine import frameEngine

################################
class frameActions(frameEngine):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)

    ################################
    def REPRESENT(self, mode, clear=True):
        if clear:
            self.outText.Clear()
        else:
            self.outText.AppendText('\n'*4)
        if mode == 'SEL':
            data = self.Selection
            self.outText.AppendText(lang['selection']+'\n'*2)
        if mode == 'ALL':
            data = self.AllData
            self.outText.AppendText(lang['all-data']+'\n'*2)
        data = data.drop(conf['rem-from-repr'], axis=1)
        if conf['hide-no-segn']:
            drop = data.loc[data['segn'].isin(['', 'none'])]
            data = data.drop(drop.index)
        self.outText.AppendText(data.__repr__()+'\n')

    ################################
    def action(self, event):
        self.prompt('info', 'default')

    ################################
    def actionLoadSheet(self, event, mode='std'):
        if mode == 'std':
            msg = lang['dlg']['load-s-msg']
        elif mode == 'upd':
            msg = lang['dlg']['loadu-s-msg']
        dialog = dlg.FileDialog(msg, 'csv', 'open')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            return
        dialog.Destroy()
        try:
            self.AllData = pd.read_csv(path, encoding=static['encoding-sheet'])
            self.AllData.sort_values(['segn', 'regn', 'area'], inplace=True)
            self.AllData.set_index(static['column-index'], inplace=True)
            self.AllData.replace(nan, static['empty-marker'], inplace=True)
        except pd.errors.ParserError:
            self.prompt('error', 'not-a-csv')
            return
        self.REPRESENT('ALL')

    ################################
    def actionLoadOrig(self, event, mode='std'):
        if mode == 'std':
            msg = lang['dlg']['load-o-msg']
        elif mode == 'upd':
            msg = lang['dlg']['loadu-o-msg']
        dlg = wx.DirDialog(self,
            message=msg,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            return
        self.AllData = self.EngineLoad(path)
        self.AllData.sort_values(['segn', 'regn', 'area'], inplace=True)
        self.REPRESENT('ALL')

    ################################
    def actionLoadUpdSheet(self, event):
        try:
            old = self.AllData
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            return
        self.actionLoadSheet(event, 'upd')
        old.update(self.AllData)
        self.AllData = old
        self.REPRESENT('ALL')

    ################################
    def actionLoadUpdOrig(self, event):
        try:
            old = self.AllData
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            return
        self.actionLoadOrig(event, 'upd')
        old.update(self.AllData)
        self.AllData = old
        self.REPRESENT('ALL')

    ################################
    def actionSaveSheet(self, event):
        try:
            self.AllData
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            return
        msg = lang['dlg']['save-s-msg']
        dialog = dlg.FileDialog(msg, 'csv', 'save')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            return
        dialog.Destroy()
        self.AllData.to_csv(path, encoding=static['encoding-sheet'])

    ################################
    def actionSaveOrig(self, event):
        try:
            self.AllData
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            return
        msg = lang['dlg']['save-o-msg']
        dlg = wx.DirDialog(self,
            message=msg,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            return
        self.EngineSave(path)

    ################################
    def actionSELECT(self, mode):
        # Check if can continue
        if mode in ['new', 'app']:
            try:
                self.AllData
            except AttributeError:
                self.prompt('warning', 'data-not-loaded')
                return 0
            src = self.AllData
        elif mode in ['sub', 'app']:
            try:
                self.Selection
            except AttributeError:
                self.prompt('warning', 'data-not-slctd')
                return 0
        ################
        # Action
        if mode == 'sub':
            src = self.Selection
        d = dlg.SelectDialog('selection-'+mode, src)
        if d.ShowModal() == wx.ID_OK:
            condCol = d.col.GetString(d.col.GetSelection())
            condAttrs = d.attrList.GetCheckedStrings()
            NEW = src.loc[src[condCol].isin(condAttrs)]
        else:
            return 0
        return NEW

    ################################
    def actionSelectNew(self, event):
        NEW = self.actionSELECT('new')
        if type(NEW) == int:
            return
        self.Selection = NEW
        self.REPRESENT('SEL')
    ################################
    def actionSelectSub(self, event):
        NEW = self.actionSELECT('sub')
        if type(NEW) == int:
            return
        self.Selection = NEW
        self.REPRESENT('SEL')
    ################################
    def actionSelectApp(self, event):
        NEW = self.actionSELECT('app')
        if type(NEW) == int:
            return
        self.Selection = pd.concat([self.Selection, NEW])
        self.REPRESENT('SEL')


    ################################
    def actionQuit(self, event):
        self.Close()


    # TODO (Show function desc on button hover)
    #def actionMouseEnter(self, event):
    #    self.StatusBar.PushStatusText("Button Hover")
    #    event.Skip()
    #
    #def actionMouseLeave(self, event):
    #    self.StatusBar.PopStatusText()
    #    event.Skip()
    #button.Bind(wx.EVT_ENTER_WINDOW, self.actionMouseEnter)
    #button.Bind(wx.EVT_LEAVE_WINDOW, self.actionMouseLeave)
