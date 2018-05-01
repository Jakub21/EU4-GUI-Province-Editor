################################
# Jakub21
# March 2018
# License: MIT
# Python 3.6.3

################################
from src.actions import frameActions
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class frameCommands(frameActions):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)

    ################################
    def DoCommandSet(self, path):
        Log.info('Executing command set from file: '+'/'.join(path.split('/')[-3:]))
        data = open(path, 'r').read().replace('\n', ' ')
        data = data.split('>')
        data = list(filter(lambda x: not x.startswith('#'), data))[1:]
        ################
        Log.info('Instructions count: '+str(len(data)))
        index = 0
        for command in data:
            try:
                Log.info('Command no.'+str(index))
                result = self.DoCommand(command=command, fromFile=True)
            except:
                Log.error('Uncaught error occurred ('+command+').\nRaising error')
                raise
            if not result:
                Log.info('Leaving CommandSet exe loop')
                return
            index += 1
        Log.info('Command set executed successfully')

    ################################
    def DoCommand(self, event=None, command='', fromFile=False):
        command = command.replace('[', ' [ ').replace(']', ' ] ')
        command = command.split()
        try:
            Func = command[0]
        except IndexError:
            Log.info('Empty instruction')
            return True # Empty instruction, allows continuation
        try:
            args = command[1:]
            args = list(map(lambda x: x.replace('NONE', ''), args))
            if '[' in args:
                A = []
                L = []
                inList = False
                for arg in args:
                    if arg == '[':
                        inList = True
                        continue
                    if arg == ']':
                        inList = False
                        A.append(L)
                        continue
                    if inList:
                        L.append(arg)
                    else:
                        A.append(arg)
                args = A
        except IndexError: args=[]
        if Func not in static['cmd-list']:
            Log.warn('Issued unknown command')
            self.prompt('warning', 'unknown-cmd')
            return

        ################################
        def ShowMissingArgs(Func):
            Log.info('Missing arguments for function '+Func)
            self.prompt('info', 'missing-arg', 'For function '+Func)
        ################################
        MissingArgs = False

        if Func in ['load', 'loadu', 'save', 'select', 'sort']:
            try: Type = args[0]
            except: MissingArgs = True
        if Func in ['load', 'loadu', 'save']:
            try: path = args[1][1:-1]
            except: MissingArgs = True

        if MissingArgs:
            ShowMissingArgs(Func)
            return

        if Func == 'load':
            if Type == 'sheet':
                self.LoadSheet(path, silent=fromFile)
            elif Type == 'orig':
                self.LoadOrig(path, silent=fromFile)
            else:
                Log.warn('Invalid argument')
                self.prompt('warning', 'invalid-arg')

        elif Func == 'loadu':
            if Type == 'sheet':
                self.LoadUpdSheet(path, silent=fromFile)
            elif Type == 'orig':
                self.LoadUpdOrig(path, silent=fromFile)
            else:
                Log.warn('Invalid argument')
                self.prompt('warning', 'invalid-arg')

        elif Func == 'save':
            if Type == 'sheet':
                self.SaveSheet(path)
            elif Type == 'orig':
                self.SaveOrig(path)
            else:
                Log.warn('Invalid argument')
                self.prompt('warning', 'invalid-arg')

        elif Func == 'select':
            try:
                attr = args[1]
                cols = args[2]
            except:
                ShowMissingArgs(Func)
                return
            if type(cols) == str:
                cols = [cols]
            if attr not in static['column-order']:
                Log.warn('Unknown column "'+attr+'"')
                self.prompt('warning', 'unknown-col')
                return
            if Type == 'new':
                self.SelectNew(attr, cols, silent=fromFile)
            elif Type == 'sub':
                self.SelectSub(attr, cols, silent=fromFile)
            elif Type == 'app':
                self.SelectApp(attr, cols, silent=fromFile)
            else:
                Log.warn('Invalid argument')
                self.prompt('warning', 'invalid-arg')

        elif Func == 'sort':
            if Type == 'loc':
                self.actionSortByLoc(silent=fromFile)
            elif Type == 'id':
                self.actionSortByID(silent=fromFile)
            else:
                Log.warn('Invalid argument')
                self.prompt('warning', 'invalid-arg')

        elif Func == 'set':
            try:
                attr = args[0]
                val = args[1]
            except:
                ShowMissingArgs(Func)
                return
            if attr not in static['column-order']:
                Log.warn('Unknown column "'+attr+'"')
                self.prompt('warning', 'unknown-col')
                return
            self.ModifyColumn(attr, val, silent=fromFile)

        elif Func == 'in':
            try:
                cAttr = args[0] # Condition
                cond = args[1]
                vAttr = args[2] # Value
                value = args[3]
            except:
                ShowMissingArgs(Func)
                return
            if type(cond) == str:
                cond = [cond]
            if cAttr not in static['column-order']+['prov']:
                Log.warn('Unknown column "'+cAttr+'"')
                self.prompt('warning', 'unknown-col')
                return
            if vAttr not in static['column-order']:
                Log.warn('Unknown column "'+vAttr+'"')
                self.prompt('warning', 'unknown-col')
                return
            if cAttr == 'prov':
                self.ModifyProvince(cond, vAttr, value, silent=fromFile)
            else:
                try:
                    CurrentSel = list(self.Selection.index)
                except AttributeError:
                    Log.warn('Can not do this with no data selected')
                    self.prompt('warning', 'data-not-slctd')
                    return
                self.SelectNew(cAttr, cond, silent=fromFile)
                self.ModifyColumn(vAttr, value, silent=fromFile)
                self.applyChanges()
                self.Selection = self.AllData.loc[CurrentSel,:]


        elif Func == 'repr':
            self.Represent()

        elif Func == 'exit':
            self.actionQuit()

        return True
