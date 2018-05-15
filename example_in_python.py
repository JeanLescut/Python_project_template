
# coding: utf-8

# In[1]:


import logging
import sys
import yaml


# In[2]:


logging.basicConfig(stream=sys.stdout,
                        format='[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s',
                        level=logging.DEBUG)
logging.info('Logging ready, Start of the script !')


# In[3]:


# Loading Configuration :
def load_conf_file(path_conf) :
    logging.debug(f'Loading conf file {path_conf} ...')
    try :
        return yaml.safe_load(open(path_conf, 'r'))
    except FileNotFoundError :
        logging.warning(f'The path {path_conf} does not correspond to any file !')
        return dict()
    
conf = load_conf_file('./etc/default.yml')
conf.update(load_conf_file('./etc/local.yml'))

if 'ipykernel_launcher.py' != sys.argv[0].split('/')[-1] : # If not run in Jupyter :
    for arg in sys.argv[1:] : # For every argument (conf_yaml, param_yaml, etc...)
        conf.update(load_conf_file(arg))


# In[4]:


logging.info('###########################################')
logging.info('Loading credentials stored locally...')
with open('/usr/local/share/credentials/AD','r') as creds_file:
    creds = dict([keyval.split('=') for keyval in creds_file.read().strip().split('\n')])
# Note : Never print the credentials in the log !


# # Your code start here :

# In[5]:


# First thing in the script : import all libraries at once :
import paramiko
import pymssql


# In[6]:


logging.info('###########################################')
logging.info('Example of SSH connection :')
logging.debug('Creating SSH client...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = 'chsxedwhdc001', 
            username = creds['user'],
            password = creds['pass'])

logging.debug('using SSH connection to retrieve data...')
_, stdout, _ = ssh.exec_command('whoami')
result = stdout.readline().strip()
logging.info(f'I am {result} !')


# In[8]:


logging.info('###########################################')
logging.info('Example of SQL connection :')
connection = pymssql.connect(server = 'CHCXSQLARMDM008', 
                             user = creds['domain'] + '\\' + creds['user'], 
                             password = creds['pass'], 
                             database = 'Pricing',
                             autocommit=True)
cursor = connection.cursor()

logging.debug('Executing a statement...')
query=f'SELECT 1'
logging.debug(query)
cursor.execute(query)
logging.debug(cursor.fetchall())


# In[9]:


logging.info('End of the script (success)') # Always finish by that to confirm a precocious exit did not happen

