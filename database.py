#%%
import json,zlib
import sqlite3
from functions import *
from config import *
from data import *
from datetime import datetime
con = sqlite3.connect("herald.db")
cur = con.cursor()
#%%
json_data = query(days=2)
# %%
matches = ([(i['match_id'],datetime.utcfromtimestamp(i['start_time']).strftime('%Y-%m-%d %H:%M:%S')) for i in json_data['rows']])
for m in matches:
    cur.execute("INSERT OR IGNORE INTO matches VALUES ('{}','{}')".format(m[0],m[1]))
con.commit()
#%%
con = sqlite3.connect("herald.db")
cur = con.cursor()
matches = ([i['match_id'] for i in json_data['rows']])
for i in range(0,len(matches)-10,10):
    try:
        data = query_matches(matches[i:i+10])
    except:
        continue
    match_data_list = data['data']['matches']
    leavers = stratz_remove_leavers(data)
    for m in match_data_list:
        if m['id'] not in leavers:
            json_str = json.dumps(m)
            cur.execute("INSERT OR IGNORE INTO match_info VALUES ('{}','{}','{}')".format(m['id'],datetime.utcfromtimestamp(m['startDateTime']).strftime('%Y-%m-%d %H:%M:%S'),json_str))
    con.commit()
    time.sleep(1)
