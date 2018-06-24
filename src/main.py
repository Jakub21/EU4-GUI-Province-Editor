'''Developed by Jakub21 in June 2018
License: MIT
Python version: 3.6.5
'''
from datetime import datetime
import wx
import sys
import traceback as Trb
from src.editor import Editor

import logging
Log = logging.getLogger('MainLogger')


def define_loggable_exceptions():
    '''Modify system function that shows exception info'''
    def _excepthook(type, value, traceback):
        traceback = ''.join(Trb.format_tb(traceback))
        m = 'An exception occurred:\n'+'-'*64+'\n'
        if len(traceback) > 0:
            m += 'Traceback (most recent call last):\n'+traceback+'\n'
        else:
            m += 'No traceback available\n'
        m += type.__name__+': '+str(value)
        m +='\n'+'-'*64+'\n'
        Log.error(m)
    sys.excepthook = _excepthook

def configure_logger(level):
    '''Initialize logger with both console and file handlers'''
    Log.setLevel(level)
    formatter = '[%(asctime)s][%(filename)s:%(lineno)d] %(message)s'
    formatter = logging.Formatter(formatter, '%H:%M:%S')
    ConsoleHandler = logging.StreamHandler()
    ConsoleHandler.setLevel(level)
    ConsoleHandler.setFormatter(formatter)
    Log.addHandler(ConsoleHandler)

def main(is_debug):
    '''Start Editor'''
    start_time = datetime.now()
    levels = {
        True: logging.DEBUG,
        False: logging.INFO,
    }
    define_loggable_exceptions()
    configure_logger(levels[is_debug])
    H, M, S = start_time.hour, start_time.minute, start_time.second
    Log.info('Starting Editor ('+str(H)+':'+str(M)+':'+str(S)+')')

    app = wx.App()
    frame = Editor()
    app.MainLoop()
