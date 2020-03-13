#!/usr/bin/python

__task__: '''
deps-pip:
- pip install sqlalchemy
- pip install MySQL-python
below is an example script:
'''


from sqlalchemy.engine import create_engine
import json

engine = create_engine('mysql://root:P4ssWordD@localhost/reports')

conn = engine.connect()

row = conn.execute("select * from updatestatus")
json_result = []

for result in row:
        d = {'ORG_ID': result['org_id'],
           'ORG_NAME': result['orgname'],
           'LAST_UPDATED': result['last_update_time'],
           'NEXT_UPDATE': result['next_update_time'],
           'MACHINE': result['Machine'],
           'FREQUENCY': result['Frequency'],
           'REGION': result['Cluster'],
           'SYNC_TIME': result['Total Time']}
        json_result.append(d)

interm_result = {"data" : json_result}
final_result = json.dumps(interm_result, default=str, indent=4)

#if you dont use defaul=str , you will get error "datetime.datetime(2015, 6, 10, 14, 14, 37) is not JSON serializable" if you use
#datetime format results from mysql.


print(final_result)
