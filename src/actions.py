################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx


################################
class frameActions(wx.Frame):
    def __init__(self, _conf, _lang):
        super().__init__(None)
        global lang
        lang = _lang
        global conf
        conf = _conf

    def action(self, event):
        print('DEFAULT-ACTION')

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
