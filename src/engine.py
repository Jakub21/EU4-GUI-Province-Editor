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
import logging

################################
Log = logging.getLogger('MainLogger')

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
        key         = ''
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
            if len(text) == 1:
                return text[0]
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
                    return static['mlt-sep'].join(text)
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
    def EngineLoad(self, path, limit):
        Log.info('Starting Load procedure')
        ################
        def GetValue(keys, data):
            if len(keys) == 1:
                result = data[keys[0]]
            else:
                q = []
                for sub in data[keys[0]]:
                    q += GetValue(keys[1:], sub)
                return q
            if result in [['nan'], ['no']]:
                result = ''
            return result
        ################
        def GetID(filename):
            numbers = ''.join(map(lambda x: str(x), range(10)))
            result = ''
            for c in filename:
                if c not in numbers:
                    break
                result += c
            return result
        ################
        def LoadScope(contents, province={k:'' for k in static['column-order']}):
            for dataKey in static['history-file-keys'].keys():
                fileKey = static['history-file-keys'][dataKey]
                if type(fileKey) != list: fileKey = [fileKey]
                try: province[dataKey] = GetValue(fileKey, contents)
                except KeyError: pass
            return province
        ################
        total_provs = len(listdir(path))
        d = Progress('load', 'load-desc', '', total_provs, parent=self)
        Y, M, D = 0,1,2
        GetDate = lambda x: (tuple(map(lambda q: int(q), x.split('.'))))
        NotADate = {}
        rows = []
        i=0
        ################################
        for filename in listdir(path):
            if not d.Update(i, 'load-desc', filename):
                d.Destroy()
                return 0
            if i % static['engine-log-rate'] == 0:
                Log.debug('Progress: '+str(100*(i/total_provs))[:4]+'%')
            t = self.EngineGetFile(path+'/'+filename)
            try:
                contents = self.EngineGetScope(t.split())
            except TypeError:
                Log.warn('Syntax Error in History File ('+filename+')')
                self.prompt('warning', 'hist-syntax', data=filename)
                continue
            i+=1
            ################
            province = LoadScope(contents)
            for key in [ k for k in contents.keys() if
                    (k not in static['history-file-keys'].values()) and
                    (k not in static['not-in-file'])
                ]:
                try:
                    date = GetDate(key)
                    if (date[Y] < limit[Y])or(
                        (date[Y] == limit[Y])and((date[M] < limit[M])or(
                            (date[M] == limit[M])and(date[D] <= limit[D])))):
                        province = LoadScope(contents[key][0], province)
                except ValueError:
                    try: NotADate[str(key)].append(str(ID))
                    except KeyError: NotADate[str(key)] = [str(ID)]
            ################
            ID = GetID(filename)
            if ID == '':
                continue
            province['id'] = int(ID)
            province['filename'] = filename
            ################
            try: province['name'] = self.Locl['PROV'+ID]
            except KeyError: province['name'] = ''
            try: province['area'] = self.Assnmt[ID][0]
            except KeyError: province['area'] = ''
            try: province['regn'] = self.Assnmt[ID][1]
            except KeyError: province['regn'] = ''
            try: province['segn'] = self.Assnmt[ID][2]
            except KeyError: province['segn'] = ''
            ################
            row = []
            for key in static['column-order']:
                value = province[key]
                if type(value) == list:
                    value = static['mlt-sep'].join(map(lambda x: str(x), value))
                if type(value) == str:
                    value = ''.join(list(filter(lambda ch: ch not in '"', value)))
                row.append(value)
            ################
            rows.append(row)
        ################
        for key in NotADate:
            Log.warn('Unsuccessful attempt to convert file-key "'+key+'" to Date in '+str(len(NotADate[key]))+' provinces')
        df = pd.DataFrame(rows, columns=static['column-order'])
        df.set_index(static['column-index'], inplace=True)
        d.Destroy()
        Log.debug('Loaded '+str(i)+' provinces.'+\
            'There are '+str(len(listdir(path)))+' files in the directory.')
        Log.info('Load procedure complete')
        return df

    ################################
    def EngineSave(self, path, onlyChanged=False):
        Log.info('Starting Save procedure')
        ################
        def SaveLine(key, value, maxdepth, depth=0):
            i = static['indent']
            result = ''
            if depth == maxdepth:
                result += i*depth+key[0]+' = '+value+'\n'
            else:
                result += i*depth+key[0]+' = {\n'
                result += SaveLine(key[1:], value, maxdepth, depth+1)
                try:
                    result += i*(depth+1)+static['save-info'][key[0]]+'\n'
                except KeyError:
                    pass # Optional
                result += i*depth + '}\n'
            return result
        ################
        def SaveList(key, values, depth=0):
            i = static['indent']
            result = i*depth+key[0]+' = {\n'+i*(depth+1)
            result += ' '.join(values)+'\n'+i*depth+'}\n'
            return result
        ################
        data = self.AllData
        try:
            IDList = data.index.values
        except AttributeError:
            self.prompt('warning', 'data-not-loaded')
            return
        ################
        data = data.values.tolist()
        columns = static['column-order'][1:]
        sep = '/'
        INDEX = 0
        if onlyChanged:
            TOTAL = self.Changed
        else:
            TOTAL = len(data)
        d = Progress('save', 'save-desc', '', TOTAL, parent=self)
        ################
        for row in data:
            ID = IDList[INDEX]
            text = static['histfile-prefix'] + str(ID) + '\n'*2
            filename = ''
            Changed = False
            for col, value in zip(columns, row):
                if static['float-to-int'] and (type(value) == float):
                    value = int(value)
                value = str(value)
                if (col == 'changed') and (value == 'yes'):
                    Changed = True
                if col == 'filename':
                    filename = value
                    continue
                if (col == 'capital') and (len(value.split()) > 1):
                    value = '"'+value+'"'
                if col not in static['history-file-keys'].keys():
                    continue
                ################
                key = static['history-file-keys'][col]
                if type(key) == str:
                    key = [key]
                ################
                if static['mlt-sep'] in value:
                    value = value.split(static['mlt-sep'])
                else:
                    value = [value]
                ################
                if (col in static['file-lists']) and (value != ['']):
                    # key = {val val}
                    text += SaveList(key, value)
                elif col not in static['file-lists']:
                    # key = val  key = val
                    for elem in value:
                        if (elem.lower() in static['EMPTY']) or (elem == ''):
                            continue
                        text += SaveLine(key, elem, len(key)-1)
            DIR = path + '/' + filename
            if Changed or not(onlyChanged):
                INDEX += 1
                if not d.Update(INDEX, 'save-desc', filename):
                    d.Destroy()
                    return
                if INDEX % static['engine-log-rate'] == 0:
                    Log.debug('Progress: '+str(100*(INDEX/TOTAL))[:4]+'%')
                try:
                    open(DIR, 'w').write(text)
                except PermissionError:
                    Log.warn('Permission denied: "'+DIR+'"')

        d.Destroy()
        Log.debug('Saved '+str(INDEX)+' out of '+str(TOTAL)+' provinces')
        Log.info('Save procedure complete')
        return True
