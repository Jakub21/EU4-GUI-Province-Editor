################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import yaml
from os import getcwd
import logging

################################
Log = logging.getLogger('MainLogger')

################################
class PATH:
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
        Log.error(FLS_ERR)
        exit()
    except yaml.YAMLError as e:
        Log.error(YML_ERR+'\n'+e)
        exit()
    except Exception as e:
        Log.error(UNH_ERR+'\n'+e)
        exit()

################################
def getstatic():
    Log.info('Loading Static')
    global static
    static = getfile(PATH.STAT)
    return static

################################
def getconf():
    Log.info('Loading Configuration')
    global conf
    conf = getfile(PATH.CONF)
    return conf

################################
def getlcl():
    Log.info('Loading Localisation')
    global lang
    lang = getfile(PATH.LANG)
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
