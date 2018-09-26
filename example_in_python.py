
# coding: utf-8

# In[ ]:


import logging, sys


# In[ ]:


logging.basicConfig(stream=sys.stdout,
                        format='[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s',
                        level=logging.WARN)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug(f'Python version = {sys.version}')
log.debug(f'argv is = {sys.argv}')


# In[ ]:


from python_utils import sql, load ,email2
logging.getLogger('python_utils').setLevel(logging.DEBUG)
conf = load.conf(sys.argv)
creds = load.creds()


# # Your code start here :

# In[ ]:


import paramiko
log.info('###########################################')
log.info('Example of SSH connection :')
log.debug('Creating SSH client...')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = 'chsxedwhdc001', 
            username = creds['AD']['user'],
            password = creds['AD']['pass'])

log.debug('using SSH connection to retrieve data...')
_, stdout, _ = ssh.exec_command('whoami')
result = stdout.readline().strip()
log.info(f'I am {result} !')


# In[ ]:


import pymssql
log.info('###########################################')
log.info('Example of SQL connection :')
def sql_conn() :
    return pymssql.connect(server = 'CHCXSQLARMDM008', 
                             user = creds['AD']['domain'] + '\\' + creds['AD']['user'], 
                             password = creds['AD']['pass'], 
                             database = 'Pricing',
                             autocommit=True)
connection=sql_conn()
cursor = connection.cursor()

log.debug('Executing a statement...')
query=f'SELECT 1'
log.debug(query)
cursor.execute(query)
log.debug(cursor.fetchall())

connection.close()


# In[ ]:


from impala.dbapi import connect 
log.info('###########################################')
log.info('Example of Hive connection :')
## Hive Connection
def hive_conn() :
    return connect(host='hiveserver2.idx.expedmz.com', port=10001, 
                    database="lz", auth_mechanism="PLAIN", 
                    user=creds['HiveServer2']['user'], password=creds['HiveServer2']['pass'])

connection=sql_conn()
cursor = connection.cursor()

log.debug('Executing a statement...')
query=f'SELECT 1'
log.debug(query)
cursor.execute(query)
log.debug(cursor.fetchall())

connection.close()


# In[ ]:


log.info('End of the script (success)') # Good practice : finish by that to confirm a clean exit

