################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from src.dialog import frameDialog, ConfigDialog
from pandas import set_option as PandasOption
from src.conf_parser import PATH
from warnings import filterwarnings
import yaml
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class frameInit(frameDialog):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)
        filterwarnings('ignore')
        Log.info('Updating Pandas settings')
        PandasOption('display.max_rows', static['pandas']['max-rows'])
        PandasOption('display.max_columns', static['pandas']['max-cols'])
        PandasOption('display.width', static['pandas']['disp-width'])
        self.initSession(static, lang)
        self.sessionInitialized = True

    ################################
    def YamlDump(self, data, path):
        text = yaml.dump(data, default_flow_style=False, indent=4)
        f = open(self.cwd+path, 'w', newline='\n')
        f.write(text)
        f.close()

    ################################
    def RemoveComments(self, text):
        ndata = ''
        for line in text.split('\n'):
            nline = ''
            for c in line:
                if c in '#\r\n':
                    break
                if c == '\t':
                    c = ' '
                if c in '{=}':
                    c = ' ' + c + ' '
                nline += c
            ndata += nline + ' '
        return ndata

    ################################
    def initAssignment(self):
        Log.info('Loading Assignments')
        ################
        def Get(self, path):
            text = None
            for enc in static['encodings']:
                try:
                    text = open(path, encoding=enc).read()
                except:
                    pass
            if text == None:
                self.prompt('error', 'filenotfound')
            return self.RemoveComments(text)
        ################
        def Analysis(text, memDepth):
            par_depth = 0
            depth = 0 # Starting
            master = 'none'
            members = []
            result = {}
            for word in text.split():
                depth += word.count('{')
                depth -= word.count('}')
                if word in static['skip-at-regload']:
                    continue
                if depth == par_depth:
                    if master != 'none':
                        result[master] = members
                    master = word
                    members = []
                if depth == memDepth:
                    members.append(word)
            return result
        ################
        def Find(searchKey, scope):
            for key in scope:
                value = scope[key]
                if searchKey in value:
                    return key
        ################
        def Shorten(name, rtype):
            suffixes = static['reg-names-suffixes']
            suffix = suffixes[rtype]
            try:
                if name.endswith(suffix):
                    name = name[:-len(suffix)]
            except AttributeError:
                name = 'none'
            return name
        ################
        segn = Analysis(Get(self, conf['path']['segn']), 1)
        regn = Analysis(Get(self, conf['path']['regn']), 2)
        area = Analysis(Get(self, conf['path']['area']), 1)
        for r in [segn, regn, area]:
            if r == {}:
                Log.error('Error occurred during Assignment loading')
                self.prompt('error', 'inv-asnmt-file')
                return False

        result = {}
        usedAreas = []
        usedRegns = []
        usedSegns = []
        for Area in area:
            Regn = Find(Area, regn)
            Segn = Find(Regn, segn)
            provs = area[Area]
            ################
            aName = Area
            rName = Regn
            sName = Segn
            ################
            if static['shorten-regn-names']:
                aName = Shorten(aName, 'area')
                rName = Shorten(rName, 'regn')
                sName = Shorten(sName, 'segn')
            ################
            for province in provs:
                result[province] = [aName, rName, sName]
                if Area not in usedAreas:
                    usedAreas.append(Area)
                if Regn not in usedRegns:
                    usedRegns.append(Regn)
                if Segn not in usedSegns:
                    usedSegns.append(Segn)
        ################
        self.unusedAreas = []
        self.unusedRegns = []
        self.unusedSegns = []
        for key in area:
            if key not in usedAreas:
                self.unusedAreas.append(key)
        for key in regn:
            if key not in usedRegns:
                self.unusedRegns.append(key)
        for key in segn:
            if key not in usedSegns:
                self.unusedSegns.append(key)
        ################
        self.Assnmt = result
        return True


    ################################
    def initLocalisation(self):
        Log.info('Loading Localisation')
        path = conf['path']['locl']
        numbers = ''.join(map(lambda x: str(x), range(10)))
        try:
            data = open(path, 'r', encoding=static['encoding-locl']).read()
            newdata = ''
            prev = ''
            for c in data:
                if (prev == ':') and (c in numbers):
                    c = ''
                newdata += c
                prev = c
            data = newdata
            q = False
            locl = yaml.load(data)
            for lang in static['locl-langs']:
                try:
                    self.Locl = locl[lang]
                    q = True
                except KeyError:
                    pass
            return q
        except yaml.YAMLError as e:
            Log.error('YAML Error occurred during Locals loading: '+str(e))
            self.prompt('error', 'locl-not-yml')
            return False
        except FileNotFoundError:
            Log.error('Localisation file was not found')
            self.prompt('error', 'locl-not-found')
            return False


    ################################
    def Configure(self, event=None):
        Log.info('Starting Configurator')
        PausedInitialization = False
        if self.busyDlg != None:
            PausedInitialization = True
            self.statusBusyEnd()
        d = ConfigDialog()
        if d.ShowModal() == wx.ID_OK:
            ################ Assignment / Localisation
            for key in conf['path'].keys():
                conf['path'][key] = d.PathStr[key].GetValue().replace('\\', '/')
            if 0 in map(lambda x: len(x), conf['path'].values()):
                self.prompt('error', 'no-conf')
                Log.info('User attempted to close Configurator with missing files')
                exit() # Can not start Editor w/o configuration
            else:
                conf['was-configured'] = True
            ################ Representation Font Size
            conf['repr-font-size'] = int(d.fontSize.GetValue())
            ################ Hidden no-segn provinces
            conf['hide-no-segn'] = d.NoSegn.GetValue()
            ################ Hidden Columns
            conf['rem-from-repr'] = list(d.hiddenCols.GetCheckedStrings())
            ################ Saving
            Log.info('Saving new configuration')
            self.YamlDump(conf, PATH.CONF)
            Log.info('Configurator done')
        else:
            Log.info('Configurator canceled')
            if not self.sessionInitialized:
                self.prompt('error', 'no-conf')
                Log.error('Configuration is invalid')
                exit() # Can not start Editor w/o configuration
        d.Destroy()
        if PausedInitialization: # Only resumes PleaseWait if it was running before
            self.statusBusyStart()
        return True

    ################################
    def initSession(self, static, lang):
        self.InitConfig = False
        Log.info('Initializing Session')
        if 0 in map(lambda x: len(x), conf['path'].values()):
            conf['was-configured'] = False
        if not conf['was-configured']:
            Log.warn('Configuration is empty or invalid')
            self.InitConfig = True
            self.Configure()

        if not self.initLocalisation():
            conf['was-configured'] = False
            self.YamlDump(conf, PATH.CONF)
        if not self.initAssignment():
            conf['was-configured'] = False
            self.YamlDump(conf, PATH.CONF)
