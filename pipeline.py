
# coding: utf-8

# In[ ]:


# First thing in the script : import all libraries at once :
import paramiko
import re
import pymssql
import logging
import sys


# In[ ]:


logging.basicConfig(stream=sys.stdout,
                        format='[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s',
                        level=logging.DEBUG)
logging.info('Logging ready, Start of the script !')


# In[ ]:


def load_bash_conf_file(path_conf) :
    def match(line) :
        m = re.match("^ *([a-zA-z0-9_]+)='(.*?)'", line) # Single quoted text
        if m is not None : return m.groups()
        m = re.match('^ *([a-zA-z0-9_]+)="(.*?)"', line) # Double quoted text
        if m is not None : return m.groups()
        m = re.match("^ *([a-zA-z0-9_]+)=([0-9]+)", line) # Int variable
        if m is not None : return (m.groups()[0], int(m.groups()[1]))
        m = re.match("^ *([a-zA-z0-9_]+)=([^ ]+)", line) # Bad practice : unquoted strings
        if m is not None : return m.groups()
        return None
    try :
        with open(path_conf,'r') as conf_file:
            return dict([ r for r in [match(line) for line in conf_file.read().split("\n")] if r is not None])
    except FileNotFoundError :
        logging.warning(f'The path {path_conf}) does not correspond to any file !')
        return dict()


# In[ ]:


logging.info('###########################################')
logging.info('Loading default configuration ...')
conf = load_bash_conf_file('./etc/default.sh')
logging.info('Try to load local configuration ...')
conf.update(load_bash_conf_file('./etc/local.sh'))
logging.info('Try to load configuration passed in parameters...')
try : 
    conf.update(load_bash_conf_file(sys.argv[1])) # Note : while running the notebook, the '-f' is passed. It is not a concern.
except IndexError :
    logging.warning('No argument seem to be passed to this script !')
logging.info(f'conf = {conf}')


# In[ ]:


logging.info('###########################################')
logging.info('Loading credentials stored locally...')
# Connecting using AD (Active Directory) credentials stored in the local server :
creds = load_bash_conf_file('/usr/local/share/credentials/AD')
# Note : Never print the credentials in the log !


# In[ ]:


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


# In[ ]:


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
cursor.fetchall()


# In[ ]:


logging.info('End of the script (success)') # Always finish by that to confirm a precocious exit did not happen

