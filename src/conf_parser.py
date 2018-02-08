################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import yaml
from os import getcwd

################################
STAT = '/conf/static.yml'
CONF = '/conf/config.yml'
LANG = '/conf/lang.yml'

################################
YML_ERR = 'Yaml Error occurred. Please check config and localisation files.'
FLS_ERR = 'Configuration or localisation file not found'
UNH_ERR = 'Unhandled error in conf_parser.py'

################################
def getfile(fname):
    try:
        path = getcwd().replace('\\', '/')+fname
        return yaml.load(open(path, 'r').read())
    except FileNotFoundError:
        print(FLS_ERR)
        exit()
    except yaml.YAMLError as e:
        print(YML_ERR, e, sep='\n')
        exit()
    except Exception as e:
        print(UNH_ERR, e, sep='\n')
        exit()

################################
def getstatic():
    global static
    static = getfile(STAT)
    return static

################################
def getconf():
    global conf
    conf = getfile(CONF)
    return conf

################################
def getlcl():
    global lang
    lang = getfile(LANG)
    return lang


################################
def getWildcard(formats, appendAll=True):
    if type(formats) != list:
        formats = [formats]
    if appendAll == True:
        formats.append('*')
    wc = ''
    wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"
    for f in formats:
        wc += lang['formats'][f] + ' (*.'+f+')|*.'+f+'| '
    wc = wc[:-2]
    return wc
