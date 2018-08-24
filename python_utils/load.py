
# coding: utf-8

# In[ ]:


import yaml
import logging
log = logging.getLogger(__name__)
log.debug('Module loaded')


# In[ ]:


def conf(argv) :
    log.info('Loading configuration files...')

    def load_conf_file(path_conf) :
        log.debug(f'Loading conf file {path_conf} ...')
        try :
            return yaml.safe_load(open(path_conf, 'r'))
        except FileNotFoundError :
            log.warning(f'The path {path_conf} does not correspond to any file !')
            return dict()

    conf = load_conf_file('./etc/default.yml')
    conf.update(load_conf_file('./etc/local.yml'))

    if 'ipykernel_launcher.py' != argv[0].split('/')[-1] : # If not run in Jupyter :
        for arg in argv[1:] : # For every argument (conf_yaml, param_yaml, etc...)
            conf.update(load_conf_file(arg))
            
    log.info('Loading configuration files... Done !')
    log.debug(f'conf = {conf}')
    return conf


# In[1]:


def creds() :
    log.info('Loading credentials...')
    creds = {}
    for techno in ['AD', 'HiveServer2'] :
        with open('/usr/local/share/credentials/'+techno,'r') as creds_file:
            creds[techno] = dict([keyval.split('=') for keyval in creds_file.read().strip().split('\n')])
    log.info('Loading credentials... Done !')
    log.warn('PLEASE NEVER PRINT CREDENTIALS IN THE LOG, OR IN A JUPYTER CELL OUTPUT')
    return creds

