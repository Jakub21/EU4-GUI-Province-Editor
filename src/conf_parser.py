################################
# Jakub21
# February 2018
# License: MIT
# Python 3.6.3

################################
import yaml
from os import getcwd

################################
CONF = '/conf/config.yml'
LCL =  '/conf/lang.yml'

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
def getconf():
    return getfile(CONF)

################################
def getlcl():
    return getfile(LCL)
