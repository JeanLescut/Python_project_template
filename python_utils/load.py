
# coding: utf-8

# In[ ]:


import yaml
import logging
log = logging.getLogger(__name__)
log.debug('Module loaded')


# In[ ]:


def load_conf_file(path_conf) :
    log.debug(f'Loading conf file {path_conf} ...')
    try :
        return yaml.safe_load(open(path_conf, 'r'))
    except FileNotFoundError :
        log.warning(f'The path {path_conf} does not correspond to any file !')
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
        for yaml_path in argv[1:] :
            d = load_conf_file(yaml_path)
            if 'ROOT' in d.keys() :
                return d['ROOT']
        return os.path.dirname(argv[0]) # This shouldn't happen,as ROOT is always defined in main.sh

def conf(argv, jupyter_ROOT=None, script_ROOT=None) :
    log.info('Loading configuration files...')
    conf = {}
    
    ROOT = get_ROOT(argv, jupyter_ROOT, script_ROOT)
    if 'ipykernel_launcher.py' != argv[0].split('/')[-1] : # If run in Jupyter :
        for arg in argv[1:] : # For every argument (conf_yaml, param_yaml, etc...)
            conf.update(load_conf_file(arg))

    conf = load_conf_file(f'{ROOT}/etc/default.yml')
    conf.update(load_conf_file(f'{ROOT}/etc/local.yml'))
    conf['ROOT'] = ROOT
          
    log.info('Loading configuration files... Done !')
    log.debug(f'conf = {conf}')
    return conf


# In[ ]:


def creds() :
    log.info('Loading credentials...')
    creds = {}
    for techno in ['AD', 'HiveServer2'] :
        with open('/usr/local/share/credentials/'+techno,'r') as creds_file:
            creds[techno] = dict([keyval.split('=') for keyval in creds_file.read().strip().split('\n')])
    log.info('Loading credentials... Done !')
    log.warn('PLEASE NEVER PRINT CREDENTIALS IN THE LOG, OR IN A JUPYTER CELL OUTPUT')
    return creds

