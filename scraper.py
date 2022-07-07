# %%
from os import stat

from torch import NoneType
from functions import *
from data import *

# %%
json_data = query(days=(60))
# %%
matches = ([i['match_id'] for i in json_data['rows']])
print(len(matches))
# %%
filtered_matches = []
for i in range(0,len(matches)-10,10):
    try:
        data = (query_matches(matches[i:i+10]))
    except:
        continue
    match_data_list = data['data']['matches']
    leavers = stratz_remove_leavers(data)
    for m in match_data_list:
        if m['id'] not in leavers:
            filtered_matches.append(m)
    for i in leavers:
        matches.remove(i)
    print(leavers)
    time.sleep(1)
# %%
print(len(filtered_matches))
# %%
get_maximums_per_player(filtered_matches,top=20)
# %%
