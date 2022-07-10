#%%
import json,zlib
import sqlite3
from functions import *
from config import *
from data import *
from datetime import datetime
#%%
json_data = query(days=6)
#%%
con = sqlite3.connect("herald.db")
cur = con.cursor()
matches = ([i['match_id'] for i in json_data['rows']])
cur.execute("SELECT matchId from match_info")
z = cur.fetchall()
parsed_ids = [d[0] for d in z]
ids = [_id for _id in matches if _id not in parsed_ids]
print(len(matches))
for i in range(0,len(matches)-10,10):
    try:
        data = query_stratz(
            matches[i:i+10],
            start_query=start_graphql_query,
            end_query=end_graphql_query
        )
    except:
        continue
    match_data_list = data['data']['matches']
    leavers = stratz_remove_leavers(data)
    for m in match_data_list:
        if m['id'] not in leavers:
            ids = get_steam_ids(m)
            cur.executemany("insert or ignore into steam_ids values (?)",ids)
            json_str = json.dumps(m)
            cur.execute("INSERT OR IGNORE INTO match_info VALUES ('{}','{}','{}')".format(m['id'],datetime.utcfromtimestamp(m['startDateTime']).strftime('%Y-%m-%d %H:%M:%S'),json_str))
    con.commit()
    time.sleep(1)
# %%
con = sqlite3.connect("herald.db")
cur = con.cursor()
cur.execute("SELECT steam_id from steam_ids")
z = cur.fetchall()
steam_ids  = [d[0] for d in z]
cur.execute("SELECT steam_id from player_info")
z = cur.fetchall()
parsed_ids = [d[0] for d in z]
ids = [_id for _id in steam_ids if _id not in parsed_ids]
print(len(ids))
for i in range(0, len(ids),1):
    try:
        player_data = query_stratz(
            [ids[i]],
            start_query=player_specific_graphql_query,
            end_query=player_specific_graphql_query_end
        )
    except:
        continue
    for player in player_data["data"]['players']:
        if player['winCount'] == 0:
            continue
        player_json_str = json.dumps(player)
        player_id = player['steamAccountId']
        cur.execute("insert or ignore into player_info values (?,?)",(player_id,player_json_str))
    con.commit()
cur.close()
# %%
con = sqlite3.connect("herald.db")
cur = con.cursor()
#cur.execute("delete from ")
z = cur.fetchall()
con.commit()
cur.close()
# %%
