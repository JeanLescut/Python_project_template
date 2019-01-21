
# coding: utf-8

# In[12]:


import json
import logging
log = logging.getLogger(__name__)
log.debug('Module loaded')


# In[ ]:


def load_conf_file(path_conf) :
    log.debug(f'Loading conf file {path_conf} ...')
    try :
        with open(path_conf, 'r') as file :
            return json.load(file)
    except FileNotFoundError as e :
        log.error(f'The path {path_conf} does not correspond to any file !')
        print(e)
    except JSONDecodeError as e:
        log.error(f'The json is not valid ! Error was :')
        print(e)
    return dict()
        
def get_ROOT(argv, jupyter_ROOT, script_ROOT) :
    # If run in Jupyter :
    if 'ipykernel_launcher.py' == argv[0].split('/')[-1] : 
        if jupyter_ROOT is not None :
            return jupyter_ROOT
        else :
            return '.'
    else :
        if script_ROOT is not None :
            return script_ROOT
        for conf_path in argv[1:] :
            d = load_conf_file(conf_path)
            if 'ROOT' in d.keys() :
                return d['ROOT']
        return os.path.dirname(argv[0]) # This shouldn't happen,as ROOT is always defined in main.sh

def conf(argv, jupyter_ROOT=None, script_ROOT=None) :
    log.info('Loading configuration files...')
    conf = {}
    
    ROOT = get_ROOT(argv, jupyter_ROOT, script_ROOT)
    if 'ipykernel_launcher.py' != argv[0].split('/')[-1] : # If run in Jupyter :
        for arg in argv[1:] : # For every argument (conf_json, param_json, etc...)
            conf.update(load_conf_file(arg))

    conf = load_conf_file(f'{ROOT}/etc/default.json')
    conf.update(load_conf_file(f'{ROOT}/etc/local.json'))
    conf['ROOT'] = ROOT
          
    log.info('Loading configuration files... Done !')
    log.debug(f'conf = {conf}')
    return conf


# In[11]:


def creds() :
    log.info('Loading credentials...')
    with open('/usr/local/share/credentials.json','r') as creds_file:
        creds = json.load(creds_file)
    log.info('Loading credentials... Done !')
    log.warn('PLEASE NEVER PRINT CREDENTIALS IN THE LOG, OR IN A JUPYTER CELL OUTPUT')
    return creds

