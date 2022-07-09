#%%
import json,zlib
import sqlite3
from functions import *
from data import *
from datetime import datetime
con = sqlite3.connect("herald.db")
cur = con.cursor()
cur.execute("SELECT info, date from match_info")
z = cur.fetchall()
con.commit()
cur.close()
# %%
filtered_matches = [json.loads(d[0]) for d in z]
# %%
get_maximums_per_player(filtered_matches,top=20, five_stacks=False)
# %%
