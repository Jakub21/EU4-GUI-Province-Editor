################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
import pandas as pd
import src.dialog as dlg
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
        except pd.errors.ParserError:
            self.prompt('error', 'not-a-csv')
            return

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

    ################################
    def actionLoadUpdSheet(self, event):
        old = self.AllData
        self.actionLoadSheet(event, 'upd')
        old.update(self.AllData)
        self.AllData = old

    ################################
    def actionLoadUpdOrig(self, event):
        old = self.AllData
        self.actionLoadOrig(event, 'upd')
        old.update(self.AllData)
        self.AllData = old

    ################################
    def actionSaveSheet(self, event):
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
    # TEMP
    def actionTempReprData(self, event):
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.max_columns', 50)
        pd.set_option('display.width', 250)
        data = self.AllData.drop(['filename', 'discovered'], axis=1)
        data = data.loc[data['regn'].isin(['polhemia', 'polabian'])]
        data.sort_values(['segn', 'regn', 'area'], inplace=True)
        print(data)

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
