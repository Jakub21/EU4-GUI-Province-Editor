################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from src.dialog import frameDialog, InitDialog
from src.conf_parser import PATH
import yaml

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
        self.initSession(static, lang)
        self.sessionInitialized = True

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
        ################
        def Get(path):
            text = None
            for enc in static['encodings']:
                try:
                    text = open(path, encoding=enc).read()
                except:
                    pass
            if text == None:
                prompt('error', 'filenotfound')
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
        segn = Analysis(Get(conf['path']['segn']), 1)
        regn = Analysis(Get(conf['path']['regn']), 2)
        area = Analysis(Get(conf['path']['area']), 1)
        for r in [segn, regn, area]:
            if r == {}:
                self.prompt('error', 'inv-asnmt-file')
                return False

        result = {}
        usedAreas = []
        usedRegns = []
        usedSegns = []
        for Area in area:
            Regn = Find(Area, regn)
            Segn = Find(Area, segn)
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
        path = conf['path']['locl']
        numbers = ''.join(map(lambda x: str(x), range(10)))
        try:
            data = open(path, 'r', encoding='UTF-8-SIG').read()
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
            self.prompt('error', 'locl-not-yml')
            return False
        except FileNotFoundError:
            self.prompt('error', 'locl-not-found')
            return False


    ################################
    def initInstallation(self, *argv):
        PausedInitialization = False
        if self.busyDlg != None:
            PausedInitialization = True
            self.statusBusyEnd()
        d = InitDialog(static, lang)
        if d.ShowModal() == wx.ID_OK:
            for key in conf['path'].keys():
                conf['path'][key] = d.pathstr[key].GetValue().replace('\\', '/')
            if 0 in map(lambda x: len(x), conf['path'].values()):
                self.prompt('error', 'no-conf')
                exit() # Can not start Editor w/o initialization
            else:
                conf['was-configured'] = True
            yaml.dump(conf, open(self.cwd+PATH.CONF, 'w'), default_flow_style=False)
        else:
            if not self.sessionInitialized:
                self.prompt('error', 'no-conf')
                exit() # Can not start Editor w/o initialization
        d.Destroy()
        if PausedInitialization: # Only resumes PleaseWait if it was running before
            self.statusBusyStart()

    ################################
    def initSession(self, static, lang):
        if 0 in map(lambda x: len(x), conf['path'].values()):
            conf['was-configured'] = False
        if not conf['was-configured']:
            self.initInstallation(static, lang)

        if not self.initLocalisation():
            exit()
        if not self.initAssignment():
            exit()
