################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import time
start_time = int(round(time.time() * 1000))

################################
import wx
from src.mainFrame import mainFrame

################################
if __name__ == '__main__':
    app = wx.App()
    f = mainFrame()
    prompt_time = f.InitSessionBegin
    done_time = f.InitSessionEnd
    ################################
    # Unreliable when initial configuration is running
    # Uncomment those to print Launch Duration Time in console
    #print('Registered Editor launch time [ms]:', done_time-start_time)
    #print('Duration of PleaseWait prompt [ms]:', done_time-prompt_time)
    ################################
    app.MainLoop()
