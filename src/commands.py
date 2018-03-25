################################
# Jakub21
# March 2018
# License: MIT
# Python 3.6.3

################################
from src.actions import frameActions
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class frameCommands(frameActions):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)

    ################################
    def DoCommandSet(self, path):
        f = open(path, 'r').read().replace('\n', ' ')
        ################
        F = ''
        C = ['[', ']']
        for c in f:
            if c in C:
                c = ' '+c+' '
            F+=c
        f = F
        ################
        f = f.split('>')
        f = list(filter(lambda x: not x.startswith('#'), f))[1:]
        f = list(map(lambda x: x.split(), f))
        Log.info('Executing commands from file ('+str(len(f))+' instructions)')
        index = 0
        for command in f:
            try:
                self.DoCommand(command=command)
            except:
                Log.info('Uncaught error occurred during attempt to execute \
                command no.'+str(index)+' ('+' '.join(command)+').\nRaising error')
                raise
            index += 1

    ################################
    def DoCommand(self, event=None, command=''):
        try:
            Func = command.split()[0]
        except IndexError:
            Log.info('Empty instruction')
            return # Empty instruction
        try:
            args = command.split()[1:]
            if '[' in args:
                A = []
                L = []
                inList = False
                for arg in args:
                    if arg == '[':
                        inList = True
                        continue
                    if arg == ']':
                        inList = False
                        A.append(L)
                        continue
                    if inList:
                        L.append(arg)
                    else:
                        A.append(arg)
                args = A
        except IndexError: args=[]
        if Func in static['cmd-list']:
            Log.debug('Issued Cmd: '+Func+' with args: '+str(args))
        else:
            Log.warn('Issued unknown command')
            return
