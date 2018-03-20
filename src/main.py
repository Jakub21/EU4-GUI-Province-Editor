################################
# Jakub21
# March 2018
# License: MIT
# Python 3.6.3

################################
from datetime import datetime
start_time = datetime.now()

################################
import wx
import logging
import sys
import os
import traceback as Trb
from src.mainFrame import mainFrame

################################
# Log paths
path        = 'logs/info.log'
pathOld     = 'logs/old.log'
pathOlder   = 'logs/older.log'


################################
def main(isDebug):
    ################################
    # Check directory
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Moving old logs
    try:
        current = open(path, 'r').read()
        open(pathOld, 'w').write(current)
    except: pass
    try:
        old = open(pathOld, 'r').read()
        open(pathOlder, 'w').write(old)
    except: pass
    open(path, 'w').write('')

    ################################
    # Logs initialization
    level = logging.INFO
    if isDebug:
        level = logging.DEBUG
    Log = logging.getLogger('MainLogger')
    Log.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d] %(message)s', '%H:%M:%S')

    ConsoleHandler = logging.StreamHandler()
    ConsoleHandler.setLevel(level)
    ConsoleHandler.setFormatter(formatter)
    Log.addHandler(ConsoleHandler)

    FileHandler = logging.FileHandler(path)
    FileHandler.setLevel(level)
    FileHandler.setFormatter(formatter)
    Log.addHandler(FileHandler)

    ################################
    # Log Uncaught Exceptions
    Original = sys.excepthook
    def excepthook(type, value, traceback):
        traceback = ''.join(Trb.format_tb(traceback))
        m = 'Uncaught exception:\n'
        if len(traceback) > 0:
            m += 'Traceback (most recent call last):\n'+traceback+'\n'
        else:
            m += 'No traceback available\n'
        m += type.__name__+': '+str(value)
        Log.error(m)
    sys.excepthook = excepthook

    ################################
    # Initialize Frame
    Log.info('Starting Editor ('+str(start_time.time())[:11]+')')
    Log.info('Debug mode: '+str(isDebug))
    app = wx.App()
    f = mainFrame(isDebug=isDebug)
    prompt_time = f.InitSessionBegin
    done_time = f.InitSessionEnd
    WasConfigurated = f.InitConfig

    ################################
    # Measure launch time
    total = done_time - start_time
    prompt = done_time - prompt_time
    if WasConfigurated:
        Log.info('Launch time measurement is unreliable because Configurator was running')
    else:
        Log.info('Registered Editor launch time [ms]: '+str(total.total_seconds())[2:-3])
        Log.info('Duration of PleaseWait prompt [ms]: '+str(prompt.total_seconds())[2:-3])

    ################################
    # Main Event Loop
    Log.info('Starting Main Loop')
    app.MainLoop()
    Log.info('MainLoop returned. Program stops')
    if isDebug:
        Log.info('Press enter to exit Debug Console')
        input()
