#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import logging
log = logging.getLogger(__name__)
log.debug('Module loaded')


# In[ ]:


def load_conf_file(path_conf) :
    log.debug(f'Trying to load conf file {path_conf} ...')
    try :
        with open(path_conf, 'r') as file :
            return json.load(file)
    except FileNotFoundError as e :
        log.warning(f'The path {path_conf} does not correspond to any file !')
    except json.JSONDecodeError as e:
        log.error(f'The json is not valid ! Error was :')
        print(e)
    return dict()

def fallback(d1, d2) :
    if type(d1) is not dict or type(d2) is not dict :
        return d1
    d = {}
    for k in set(d1.keys()).union(set(d2.keys())) :
        if (k in d1.keys()) and (k not in d2.keys()) :
            d[k] = d1[k]
        elif (k not in d1.keys()) and (k in d2.keys()) :
            d[k] = d2[k]
        else :
            d[k] = fallback(d1[k], d2[k])
    return d

def conf(argv, jupyter_ROOT=None, script_ROOT=None) :
    log.info('Loading configuration files...')
    
    log.debug('1. Arguments hard-coded in the script :')
    # If ROOT has been overriden in the script, then use that :
    if 'ipykernel_launcher.py' == argv[0].split('/')[-1]:
        if type(jupyter_ROOT) is str :
            conf = {'ROOT': jupyter_ROOT}
        else :
            conf = {'ROOT': '.'}
    else : 
        if type(script_ROOT) is str :
            conf = {'ROOT': script_ROOT}
        else :
            conf = {} # ROOT should be defined by the shell arguments of .py script...
            
    log.debug('2. (non-Jupyter) Arguments passed (by main.sh, or manually from bash) to the .py :')
    if 'ipykernel_launcher.py' != argv[0].split('/')[-1]: # If NOT run in Jupyter :
        for arg in argv[1:] : # For every argument (conf_json_path)
            if len(arg) > 0 : # skip useless empty argument ('')
                conf = fallback(conf, load_conf_file(arg))     
    if 'ROOT' not in conf.keys() :
        log.error('Something is weird, ROOT has not been passed by main.sh...')
        conf = fallback(conf, {'ROOT': os.path.dirname(argv[0])})
        
    ##### AT THAT POINT, we are sure that ROOT is in the conf !
                
    log.debug('3. Local configuration file :')
    conf = fallback(conf, load_conf_file(f'{conf["ROOT"]}/etc/local.json'))
    
    log.debug('3. Default configuration file :')
    conf = fallback(conf, load_conf_file(f'{conf["ROOT"]}/etc/default.json'))
    
    log.info('Loading configuration files... Done !')
    log.debug(f'conf = {conf}')
    return conf


# In[ ]:


def creds() :
    log.info('Loading credentials...')
    with open('/usr/local/share/credentials.json','r') as creds_file:
        creds = json.load(creds_file)
    log.info('Loading credentials... Done !')
    log.warn('PLEASE NEVER PRINT CREDENTIALS IN THE LOG, OR IN A JUPYTER CELL OUTPUT')
    return creds

