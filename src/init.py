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
    def RemoveComments(text):
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
            return RemoveComments(text)
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
        segions = Analysis(Get(conf['path']['segion']), 1)
        regions = Analysis(Get(conf['path']['region']), 2)
        areas = Analysis(Get(conf['path']['area']), 1)
        for r in [segions, regions, areas]:
            if r == {}:
                self.prompt('error', 'inv-asnmt-file')


    ################################
    def initLocalisation(self, path):
        numbers = ''.join(map(lambda x: str(x), range(10)))
        try:
            data = open(path, 'r').read()
            newdata = ''
            prev = ''
            for c in data:
                if (prev == ':') and (c in numbers):
                    c = ''
                newdata += c
                prev = c
            data = newdata
            return yaml.load(data)
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
            #if conf['was-configured']:
            #    self.prompt('warning', 'invalid-conf')
            conf['was-configured'] = False
        if not conf['was-configured']:
            self.initInstallation(static, lang)


        l = self.initLocalisation(conf['path']['locl'])
