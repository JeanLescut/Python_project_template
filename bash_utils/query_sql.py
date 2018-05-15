import sys, pymssql

query = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

print('[Python] Connectingto database...')
sql_conn = pymssql.connect('CHCXSQLARMDM008.sea.corp.expecn.com', 
                           username, 
                           password, 
                           'PricingBMLStaging', 
                           autocommit=True)
curs = sql_conn.cursor()

print('[Python] Executing query...')
curs.execute(query)


#print('Fetching result, if any...')
#curs.fetchall()





