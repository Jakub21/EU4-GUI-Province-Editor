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
        print('DEFAULT-ACTION')

    ################################
    def actionLoadSheet(self, event):
        #dlg = wx.FileDialog(self,
        #    message=lang['dlg']['ld-sh-msg'],
        #    defaultDir=self.cwd,
        #    defaultFile='',
        #    wildcard=getWildcard(['csv']),
        #    style=wx.FD_OPEN | wx.FD_CHANGE_DIR
        #)
        dialog = dlg.FileDialog(lang['dlg']['ld-sh-msg'], 'csv')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            return
        dialog.Destroy()
        try:
            self.AllData = pd.read_csv(path)
        except pd.errors.ParserError:
            self.prompt('error', 'not-a-csv')
            return

    ################################
    def actionLoadOrig(self, event):
        dlg = wx.DirDialog(self,
            message=lang['dlg']['ld-or-msg'],
            #defaultDir=self.cwd,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            return
        #self.AllData = engine.parse(path)

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
