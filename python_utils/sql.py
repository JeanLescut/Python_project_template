
# coding: utf-8

# In[ ]:


import logging
import pymssql, pandas
import sys
log = logging.getLogger(__name__)
log.debug('Module loaded')


# ### query()
# 
# Example :
# ```
# server = 'CHCXSQLARMDM008'
# db = 'Pricing'
# query = 'SELECT 1'
# sql.query(server, db, query, creds)
# ```

# In[ ]:


def query(server, db, query, creds):
    log.debug(f'About to launch query {query}')
    
    connection = pymssql.connect(server, 
                                 creds['domain']+'\\'+creds['user'], 
                                 creds['pass'], 
                                 db, 
                                 autocommit=True)
    
    log.debug('Connected to SQL. Executing query... (please wait)')
    data = pandas.read_sql(query, connection)
    connection.commit()
    connection.close()
    
    log.debug(f'Done ! (and connection closed)')
    return data

