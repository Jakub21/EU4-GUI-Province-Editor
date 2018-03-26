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
import logging

################################
Log = logging.getLogger('MainLogger')

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
    def checkAllData(self):
        try:
            self.AllData
            return True
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            Log.warn('AllData does not exist')
            return False
    ################################
    def checkSelection(self):
        try:
            self.Selection
            return True
        except AttributeError:
            self.prompt('warning', 'data-not-slctd')
            Log.warn('AllData does not exist')
            return False
    ################################
    def applyChanges(self):
        try:
            self.AllData.update(self.Selection)
            Log.info('Changes applied successfully')
            return True
        except:
            Log.info('Could not apply changes')
            return False



    ################################
    def Represent(self, event=None, clear=True):
        if clear:
            self.outText.Clear()
        else:
            self.outText.AppendText('\n'*4)
        try:
            data = self.Selection
            self.outText.AppendText(lang['selection']+'\n'*2)
        except:
            data = self.AllData
            self.outText.AppendText(lang['all-data']+'\n'*2)
        data = data.drop(conf['rem-from-repr'], axis=1)
        if conf['hide-no-segn']:
            drop = data.loc[data['segn'].isin(['', 'none'])]
            data = data.drop(drop.index)
        self.outText.AppendText(data.__repr__()+'\n')



    ################################
    def action(self, event=None):
        Log.info('Action is not assigned')
        self.prompt('info', 'default')



    ################################
    def actionGetCommands(self, event=None):
        Log.info('GetCommands UserInput')
        dialog = dlg.FileDialog(lang['dlg']['comm-selfile'], 'euge', 'open')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            Log.info('Loading Canceled')
            return
        dialog.Destroy()
        self.GetCommands(path)
    ################################
    def GetCommands(self, path):
        Log.info('Loading command set from file')
        self.DoCommandSet(path)



    ################################
    def actionExeCmd(self, event=None):
        self.ExeCmd()
    ################################
    def ExeCmd(self):
        command = self.cmdLine.GetValue()
        Log.info('Command: '+command)
        self.cmdLine.Clear()
        self.DoCommand(command=command)



    ################################
    def actionLoadSheet(self, event=None, silent=False):
        Log.info('LoadSheet User Input')
        msg = lang['dlg']['load-s-msg']
        dialog = dlg.FileDialog(msg, 'csv', 'open')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            Log.info('User cancelled')
            return
        dialog.Destroy()
        self.LoadSheet(path, silent=silent)
    ################################
    def LoadSheet(self, path, silent=False):
        Log.info('Loading Sheet')
        try:
            self.AllData = pd.read_csv(path, encoding=static['encoding-sheet'])
            self.AllData.sort_values(['segn', 'regn', 'area'], inplace=True)
            self.AllData.set_index(static['column-index'], inplace=True)
            self.AllData.replace(nan, static['empty-marker'], inplace=True)
        except pd.errors.ParserError:
            Log.warn('Loading Canceled, File is not a valid CSV Spreadsheet')
            self.prompt('error', 'not-a-csv')
            return
        if not silent:
            self.Represent()
        return True



    ################################
    def actionLoadOrig(self, event=None, silent=False):
        Log.info('LoadOrig User Input')
        msg = lang['dlg']['load-o-msg']
        dlg = wx.DirDialog(self,
            message=msg,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            Log.info('Loading Canceled')
            return
        dlg.Destroy()
        self.LoadOrig(path, silent=silent)
    ################################
    def LoadOrig(self, path, silent=False):
        Log.info('Loading Original')
        Data = self.EngineLoad(path)
        if type(Data) != int:
            self.AllData = Data
        else:
            Log.info('Loading Canceled')
            return
        self.AllData.sort_values(static['sortby-loct-cols'], inplace=True)
        if not silent:
            self.Represent()
        return True



    ################################
    def actionLoadUpdSheet(self, event=None, silent=False):
        Log.info('LoadUpdSheet User Input')
        msg = lang['dlg']['loadu-o-msg']
        dialog = dlg.FileDialog(msg, 'csv', 'open')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            Log.info('User cancelled')
            return
        dialog.Destroy()
        self.LoadUpdSheet(path, silent=silent)
    ################################
    def LoadUpdSheet(self, path, silent=False):
        Log.info('Updating with Sheet')
        if not self.checkAllData(): return
        try:
            Data = pd.read_csv(path, encoding=static['encoding-sheet'])
            Data.sort_values(['segn', 'regn', 'area'], inplace=True)
            Data.set_index(static['column-index'], inplace=True)
            Data.replace(nan, static['empty-marker'], inplace=True)
        except pd.errors.ParserError:
            Log.warn('Updating Canceled, File is not a valid CSV Spreadsheet')
            self.prompt('error', 'not-a-csv')
            return
        self.AllData.update(Data)
        if not silent:
            self.Represent()
        return True



    ################################
    def actionLoadUpdOrig(self, event=None, silent=False):
        Log.info('LoadUpdOrig User Input')
        msg = lang['dlg']['loadu-o-msg']
        dlg = wx.DirDialog(self,
            message=msg,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            Log.info('Loading Canceled')
            return
        self.LoadUpdOrig(path, silent=silent)
    ################################
    def LoadUpdOrig(self, path, silent=False):
        Log.info('Updating with Original')
        Data = self.EngineLoad(path)
        if type(Data) == int:
            Log.info('Updating Canceled')
            return
        Data.sort_values(static['sortby-loct-cols'], inplace=True)
        self.AllData.update(Data)
        if not silent:
            self.Represent()
        return True



    ################################
    def actionSaveSheet(self, event=None):
        Log.info('SaveSheet User Input')
        if not self.checkAllData(): return
        msg = lang['dlg']['save-s-msg']
        dialog = dlg.FileDialog(msg, 'csv', 'save')
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0].replace('\\', '/')
        else:
            Log.info('Saving canceled')
            return
        dialog.Destroy()
        self.SaveSheet(path)
    ################################
    def SaveSheet(self, path):
        Log.info('Saving sheet')
        self.AllData.to_csv(path, encoding=static['encoding-sheet'])



    ################################
    def actionSaveOrig(self, event=None):
        Log.info('SaveOrig User Input')
        if not self.checkAllData(): return
        Log.info('Saving original')
        msg = lang['dlg']['save-o-msg']
        dlg = wx.DirDialog(self,
            message=msg,
            defaultPath=self.cwd,
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath().replace('\\', '/')
        else:
            Log.info('Saving canceled')
            return
        dlg.Destroy()
        self.SaveOrig(path)
    ################################
    def SaveOrig(self, path):
        Log.info('Saving Orig')
        if not self.checkAllData(): return
        self.EngineSave(path)



    ################################
    def actionSelectNew(self, event=None, silent=False):
        Log.info('SelectNew User Input')
        self.applyChanges()
        if not self.checkAllData(): return

        d = dlg.SelectDialog('selection-new', self.AllData)
        if d.ShowModal() == wx.ID_OK:
            attr = d.ListCol.GetString(d.ListCol.GetSelection())
            cols = d.AttrList.GetCheckedStrings()
        else:
            Log.info('Selection change canceled')
            return 0
        self.SelectNew(attr, cols, silent=silent)
    ################################
    def SelectNew(self, attr, cols, silent=False):
        Log.info('Selection: New')
        if not self.checkAllData(): return
        self.applyChanges()
        self.Selection = self.AllData.loc[self.AllData[attr].isin(cols)]
        if not silent:
            self.Represent()



    ################################
    def actionSelectSub(self, event=None, silent=False):
        Log.info('SelectSub User Input')
        self.applyChanges()
        if not self.checkSelection(): return

        d = dlg.SelectDialog('selection-sub', self.Selection)
        if d.ShowModal() == wx.ID_OK:
            attr = d.ListCol.GetString(d.ListCol.GetSelection())
            cols = d.AttrList.GetCheckedStrings()
        else:
            Log.info('Selection change canceled')
            return 0
        self.SelectSub(attr, cols, silent=silent)
    ################################
    def SelectSub(self, attr, cols, silent=False):
        Log.info('Selection: Sub')
        if not self.checkSelection(): return
        self.applyChanges()
        self.Selection = self.Selection.loc[self.Selection[attr].isin(cols)]
        if not silent:
            self.Represent()



    ################################
    def actionSelectApp(self, event=None, silent=False):
        Log.info('SelectApp User Input')
        self.applyChanges()
        if not self.checkSelection(): return

        d = dlg.SelectDialog('selection-app', self.AllData)
        if d.ShowModal() == wx.ID_OK:
            attr = d.ListCol.GetString(d.ListCol.GetSelection())
            cols = d.AttrList.GetCheckedStrings()
        else:
            Log.info('Selection change canceled')
            return 0
        self.SelectApp(attr, cols, silent=silent)
    ################################
    def SelectApp(self, attr, cols, silent=False):
        Log.info('Selection: App')
        if not self.checkSelection(): return
        self.applyChanges()
        New = self.AllData.loc[self.AllData[attr].isin(cols)]
        self.Selection = pd.concat([self.Selection, New])
        if not silent:
            self.Represent()



    ################################
    def actionSortByID(self, event=None, silent=False):
        Log.info('Sorting by ID')
        try: self.Selection.sort_index(inplace=True)
        except: pass
        try: self.AllData.sort_index(inplace=True)
        except: pass
        if not silent:
            self.Represent()



    ################################
    def actionSortByLoc(self, event=None, silent=False):
        Log.info('Sorting by Location')
        COLS = static['sortby-loct-cols']
        try: self.Selection.sort_values(COLS, inplace=True)
        except: pass
        try: self.AllData.sort_values(COLS, inplace=True)
        except: pass
        if not silent:
            self.Represent()



    ################################
    def actionModifyColumn(self, event=None, silent=False):
        Log.info('ModifyingColumn User Input')
        if not self.checkSelection(): return
        d = dlg.ModifyDialog('modify-col', self.Selection)
        if d.ShowModal() == wx.ID_OK:
            COL = d.ListCol.GetString(d.ListCol.GetSelection())
            VAL = d.AttrList.GetString(d.AttrList.GetSelection())
            if VAL == lang['other']:
                VAL = d.OtherName.GetValue()
        else:
            return
        self.ModifyColumn(COL, VAL, silent=silent)
    ################################
    def ModifyColumn(self, COL, VAL, silent=False):
        Log.info('Modifying column')
        if not self.checkSelection(): return
        self.Selection.loc[:, COL] = VAL
        if not silent:
            self.Represent()


    ################################
    def actionModifyProvince(self, event=None, silent=False):
        Log.info('ModifyProvince User Input')
        if not self.checkSelection(): return
        d = dlg.ModifyDialog('modify-prov', self.Selection)
        if d.ShowModal() == wx.ID_OK:
            COL = d.ListCol.GetString(d.ListCol.GetSelection())
            VAL = d.AttrList.GetString(d.AttrList.GetSelection())
            ROW = d.ProvInput.GetValue().split()
            if VAL == lang['other']:
                VAL = d.OtherName.GetValue()
        else: return
        self.ModifyProvince(ROW, COL, VAL, silent=silent)
    ################################
    def ModifyProvince(self, IDS, COL, VAL, silent=False):
        Log.info('Modifying province')
        if not self.checkSelection(): return
        try:
            IDS = list(map(lambda x: int(x), IDS))
        except ValueError:
            Log.warn('Province ID must be convertable to INT type', ROW.split())
            self.prompt('error', 'unknown-prov')
            return
        if False in map(lambda x: x in self.Selection.index, IDS):
            Log.warn('One of the provinces is not in selected scope')
        Log.info(IDS)
        for ID in IDS:
            self.Selection.loc[ID, COL] = VAL
        if not silent:
            self.Represent()




    ################################
    def actionQuit(self, event=None):
        Log.info('Quit Action')
        super().Close()
