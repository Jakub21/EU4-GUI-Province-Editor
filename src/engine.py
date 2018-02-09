################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import wx
import pandas as pd
from src.init import frameInit

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
    def EngineGetFile(path):
        for enc in static['encodings']:
            try:
                text = open(fpath, encoding=enc).read()
            except UnicodeDecodeError:
                pass
            except FileNotFoundError:
                prompt('error', 'filenotfound')
        return rem_cmnt(text)

    ################################
    def EngineGetScope(text, rDepth=0):
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
        if rcr_depth > 0:
            index = rcr_index
        ################
        for word in data:
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
                    return total_index
            elif index == val_index:
                if not last:
                    value = word
                if inquotes:
                    continue
                ################
                if value == cbr:
                    index = (index+1)%3
                    subscope = subscope[ssc_cuthead:]
                    value = getscope(subscope, rcr_depth+1)
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
    def EngineLoad():
        def getvalue(keys, data):
            if len(keys) == 1:
                return data[keys[0]]
            else:
                q = []
                for sub in data[keys[0]]:
                    q += getvalue(keys[1:], sub)
                if q == 'nan':
                    q = ''
                return q
        ################
        def getid(filename):
            result = ''
            for c in filename:
                if c not in numbers:
                    break
                result += c
            return result
        ################
        sep = '/'
        ################
        #regioning = get_regioning(attrdir, const['fnames'])
        #localisation = get_locl(attrdir+const['fnames']['provloc'])
        #if localisation == None:
        #    print('LocalisationNotFound')
        #    return DataFrame
        ################
        provkeys = const['province_attr_keys']
        rows = []
        ################
        try:
            filelist = listdir(histdir)
        except FileNotFoundError:
            #print('DirectoryNotFound')
            return DataFrame
        for filename in filelist:
            filedir = histdir + filename
            data = getscope(getfile(filedir).split())
            if type(data) == int:
                #print('WrongHistorySyntax')
                return DataFrame
            ################
            province = {}
            provid = getid(filename)
            if provid == '':
                continue
            province[provkeys['id']] = int(provid)
            province[provkeys['fn']] = filename
            province[provkeys['gr']] = ''
            ################################
            #try:
            #    province[provkeys['nm']] = localisation[const['locl_key_prefix']+provid]
            #except KeyError: province[provkeys['nm']] = const['default_name']
            #try:
            #    province[provkeys['ar']] = regioning[provid][0]
            #except KeyError: province[provkeys['ar']] = const['default_area']
            #try:
            #    province[provkeys['rg']] = regioning[provid][1]
            #except KeyError: province[provkeys['rg']] = const['default_region']
            #try:
            #    province[provkeys['sg']] = regioning[provid][2]
            #except KeyError: province[provkeys['sg']] = const['default_segion']
            ################################
            for datakey in const['historyfile_keys']:
                provkey = const['historyfile_keys'][datakey]
                if type(provkey) == list:   keys = provkey
                else:                       keys = [provkey]
                try:                        value = getvalue(keys, data)
                except KeyError:            value = []
                province[datakey] = value
            ################
            row = []
            for key in const['column_order']:
                value = province[key]
                if type(value) == list:
                    row.append(const['multival_sep'].join(value))
                else:
                    row.append(value)
            rows.append(row)
        ################
        df = DataFrame(rows, columns=const['column_order'])
        df.set_index(const['index_column'], inplace=True)
        return df

    ################################
    def EngineParse(path):
        total_provs = 5
        repr_dir = '/'.join(path.split('/')[-2:])
        q = prgDlg('load', 'load-desc', repr_dir, total_provs)
        ################################

        ################################
        q.Destroy()
