################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from src.dialog import frameDialog, InitDialog


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


    ################################
    def initLocalisation(self, path):
        pass


    ################################
    def initInstallation(*argv):
        d = InitDialog(static, lang)
        if d.ShowModal() == wx.ID_OK:
            print('Applying')
        d.Destroy()

    ################################
    def initSession(self, static, lang):
        if 0 in map(lambda x: len(x), conf['path'].values()):
                print('Overwritting "was-configured" variable due to empty paths')
                conf['was-configured'] = False
        if not conf['was-configured']:
            self.initInstallation(static, lang)

        #self.Localisation = self.initLocalisation(static['path']['locl'])
