################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
from src.mainFrame import mainFrame

################################
if __name__ == '__main__':
    app = wx.App()
    f = mainFrame()
    app.MainLoop()
