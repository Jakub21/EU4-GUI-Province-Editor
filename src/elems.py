################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from os import getcwd
import logging

################################
Log = logging.getLogger('MainLogger')

################################
def init(core, locl):
    Log.info('Initializing UI elements')
    global CORE, LOCL
    CORE, LOCL = core, locl

################################
class TextCtrl(wx.TextCtrl):
    def __init__(self, parent, value=''):
        super().__init__(parent)
        self.SetValue(value)
        self.SetInsertionPoint(self.GetInsertionPoint())

################################
class Button(wx.Button):
    def __init__(self, parent, key, action=None, id=0):
        try:
            label = LOCL[key]
        except KeyError:
            label = 'LOCL['+str(key)+']'
        super().__init__(parent,
            label=label,
            id=id,
            size=(CORE['btt-width'], CORE['btt-height'])
        )
        if action != None:
            self.Bind(wx.EVT_BUTTON, action)
