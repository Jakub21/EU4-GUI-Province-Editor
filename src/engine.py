################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
import pandas as pd
from src.init import frameInit
from os import listdir
from src.dialog import ProgressDialog as Progress

################################
class frameEngine(frameInit):
    def __init__(self, _stt, _lang, _conf):
        global static
        static = _stt
        global lang
        lang = _lang
        global conf
        conf = _conf
        super().__init__(static, lang, conf)

    ################################
    def EngineGetFile(self, path):
        for enc in static['encodings']:
            try:
                text = open(path, encoding=enc).read()
            except UnicodeDecodeError:
                pass
            except FileNotFoundError:
                self.prompt('error', 'filenotfound')
        return self.RemoveComments(text)

    ################################
    def EngineGetScope(self, text, rDepth=0):
        # Config
        key_index   = 0
        eqs_index   = 1
        val_index   = 2
        index       = 0     # Base index correction
        rcr_index   = 0     # InDepth index correction
        ssc_cuthead = 1     # How many words remove from subscope head
        depth       = 0
        total_index = 0
        key         = 'none'
        value       = ''
        inquotes    = False
        quoted      = ''
        obr         = '{'
        cbr         = '}'
        eqs         = '='
        quo         = '"'
        sep         = ' ' # For quoted text
        ################
        result = {}
        subscope = []
        ################
        if rDepth > 0:
            index = rcr_index
        ################
        for word in text:
            last = False
            fromsub = False
            ################
            if word == obr:
                depth += 1
            elif word == cbr:
                depth -= 1
            ################
            if depth == 0:
                if word != cbr:
                    subscope = []
            else:
                subscope.append(word)
                continue
            ################
            if word.count(quo) == 1:
                inquotes = not inquotes
                if inquotes:
                    quoted = ''
                else:
                    last = True
            ################
            if inquotes:
                quoted += word + sep
            ################
            if last:
                quoted += word
                value = quoted
            ################
            if index == key_index:
                key = word
            elif index == eqs_index:
                if word != eqs:
                    raise TypeError
            elif index == val_index:
                if not last:
                    value = word
                if inquotes:
                    continue
                ################
                if value == cbr:
                    index = (index+1)%3
                    subscope = subscope[ssc_cuthead:]
                    value = self.EngineGetScope(subscope, rDepth+1)
                    fromsub = True
                try:
                    result[key].append(value)
                except KeyError:
                    result[key] = [value]
            ################
            if not fromsub:
                index = (index+1)%3
            total_index += 1
        return result

    ################################
    def EngineLoad(self, path):
        total_provs = len(listdir(path))
        d = Progress('load', 'load-desc', '', total_provs, parent=self)
        i=0
        ################################
        for filename in listdir(path):
            if not d.Update(i, 'load-desc', filename):
                d.Destroy()
                return
            t = self.EngineGetFile(path+'/'+filename)
            try:
                contents = self.EngineGetScope(t.split())
            except TypeError:
                d.Destroy()
                self.prompt('warning', 'hist-syntax', data=filename)
                return
            i+=1
        ################################
        d.Destroy()
