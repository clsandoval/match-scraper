#%%
import json,zlib
import sqlite3
from functions import *
from data import *
from datetime import datetime
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
get_match_dict(filtered_matches,top=20, five_stacks=False,game_mode="RANDOM_DRAFT" )
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
