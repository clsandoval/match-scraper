#%%
import json,zlib
import sqlite3
from functions import *
from data import *
from datetime import datetime,timedelta
now = datetime.now().timestamp()
replay_expiry_limit = (datetime.now() - timedelta(days=6)).timestamp()
#%%
con = sqlite3.connect("herald.db")
cur = con.cursor()
cur.execute("SELECT info, date from match_info")
z = cur.fetchall()
con.commit()
cur.close()
# %%
filtered_matches = [json.loads(d[0]) for d in z]
# %%
print(len(filtered_matches))
# %%
get_match_dict(filtered_matches,top=20, five_stacks=False,time_now = replay_expiry_limit,max_rank = 20)
# %%
con = sqlite3.connect("herald.db")
cur = con.cursor()
cur.execute("SELECT info from player_info")
z = cur.fetchall()
con.commit()
cur.close()
filtered_players = [json.loads(d[0]) for d in z]
print(len(filtered_players))
x = get_player_dict(filtered_players,top=20, five_stacks=False)
# %%
x
# %%
