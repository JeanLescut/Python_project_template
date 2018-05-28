
# coding: utf-8

# In[1]:


import logging, sys


# In[2]:


logging.basicConfig(stream=sys.stdout,
                        format='[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s',
                        level=logging.WARN)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug(f'Python version = {str(sys.version)}')
log.debug(f'argv[0] is = {str(sys.argv[0])}')


# In[3]:


sys.path.append('.')
from python_utils import email, sql, load
logging.getLogger('python_utils').setLevel(logging.DEBUG)
conf = load.conf(sys.argv)
creds = load.creds()


# # Your code start here :

# In[4]:


# First thing in the script : import all libraries at once :
import paramiko
import pymssql


# In[5]:


log.info('###########################################')
log.info('Example of SSH connection :')
log.debug('Creating SSH client...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = 'chsxedwhdc001', 
            username = creds['user'],
            password = creds['pass'])

log.debug('using SSH connection to retrieve data...')
_, stdout, _ = ssh.exec_command('whoami')
result = stdout.readline().strip()
log.info(f'I am {result} !')


# In[6]:


log.info('###########################################')
log.info('Example of SQL connection :')
connection = pymssql.connect(server = 'CHCXSQLARMDM008', 
                             user = creds['domain'] + '\\' + creds['user'], 
                             password = creds['pass'], 
                             database = 'Pricing',
                             autocommit=True)
cursor = connection.cursor()

log.debug('Executing a statement...')
query=f'SELECT 1'
log.debug(query)
cursor.execute(query)
log.debug(cursor.fetchall())


# In[7]:


log.info('End of the script (success)') # Good practice : finish by that to confirm a clean exit

