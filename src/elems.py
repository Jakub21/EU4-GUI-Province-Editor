################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from os import getcwd
from src.conf_parser import getWildcard
################################
def init(_static, _lang, _conf):
    global static
    static = _static
    global lang
    lang = _lang
    global conf
    conf = _conf


################################
class TextCtrl(wx.TextCtrl):
    def __init__(self, parent, value='', modifier=6):
        super().__init__(parent,
            value=value,
            size=(modifier*static['cell-x'], static['cell-y'])
        )

################################
class Button(wx.Button):
    def __init__(self, parent, label, action=None, id=0):
        super().__init__(parent,
            label=lang['mb'][label],
            id=id,
            size=(static['cell-x'], static['cell-y'])
        )
        if action != None:
            self.Bind(wx.EVT_BUTTON, action)
