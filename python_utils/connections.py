
# coding: utf-8

# In[ ]:


import logging
import pandas as pd
#import sys
log = logging.getLogger(__name__)
log.debug('Module loaded')


# ## SQL Connection
# 
# Usage :
# ```
# query = 'SELECT 1'
# sql_query(query, creds)
# ```

# In[3]:


def get_sql_conn(creds, server='CHCXSQLARMDM008', db='Pricing'):
    # Import in function to avoid useless dependecies for project that doesnt use SQL
    import pymssql
    return pymssql.connect(server, 
                           creds['AD']['domain']+'\\'+creds['AD']['user'], 
                           creds['AD']['pass'], 
                           db, 
                           autocommit=True)


# In[4]:


def sql_query(query, creds, method='execute', server='CHCXSQLARMDM008', db='Pricing'):
    log.debug(f'SQL : About to launch query {query}')
    
    connection = get_sql_conn(creds, server, db)
    log.debug('Connected to SQL. Executing query... (please wait)')
    if 'execute'==method :
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
    elif 'pandas.read'==method :
        data = pd.read_sql(query, connection)
    connection.commit()
    connection.close()
    
    log.debug(f'Done ! (and connection closed)')
    if 'pandas.read'==method :
        return data
    else :
        return True


# ## Hive Connection
# 
# Usage :
# ```
# query = 'SELECT 1'
# hive_query(query, creds)
# ```

# In[ ]:


def get_hive_conn(creds, server='hiveserver2.idx.expedmz.com', port=10001, db="lz") :
    # Import in function to avoid useless dependecies for project that doesnt use Hive)
    from impala.dbapi import connect # To connect to Hive 
    
    return connect(host=server, port=port, 
                    database=db, auth_mechanism="PLAIN", 
                    user=creds['HiveServer2']['user'], password=creds['HiveServer2']['pass'])


# In[ ]:


def hive_query(query, creds, method='execute', server='hiveserver2.idx.expedmz.com', port=10001, db="lz") :
    log.debug(f'Hive : About to launch query {query}')
    
    connection = get_hive_conn(creds, server, port, db)
    log.debug('Connected to Hive. Executing query... (please wait)')
    if 'execute'==method :
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
    elif 'pandas.read'==method :
        data = pd.read_sql(query, connection)
    connection.commit()
    connection.close()
    
    log.debug(f'Done ! (and connection closed)')
    if 'pandas.read'==method :
        return data
    else :
        return True


# ## S3 Connection and S3 helpers

# In[ ]:


def df_to_s3(df, s3_key, s3_bucket='arm-ro-lz', fmt='parquet', engine='pyarrow', compression='snappy') :
    import boto3
    import os
    
    filename_suffix = f'.{compression}.{fmt}' if fmt=='parquet' else f'.{fmt}'
    
    temp_filename  = s3_key.split('/')[-1]
    temp_filename += filename_suffix
    local_path = f"./tmp/{temp_filename}"
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))
        
    if fmt=='parquet' :
        df.to_parquet(local_path, engine=engine, compression=compression)
    elif fmt=='csv' :
        df.to_csv(local_path)
        
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(local_path, s3_bucket, s3_key+filename_suffix)
    log.info(f'{s3_key+filename_suffix} was successfully written !')
    #os.remove(local_path)
    #log.debug(f'{local_path} has been removed (to be clean)')

