#%%
import threading
import json,zlib
import sqlite3
import queue
import tqdm
from functions import *
from config import *
from data import *
from datetime import datetime
#%%
cv = threading.Condition()
gq = queue.Queue()


def data_producer_thread(matches):
    if len(matches) == 0:
        gq.put(None)
    data = query_stratz(matches)
    gq.put(data)
    with cv:
        cv.notify()


def data_consumer_thread():
    con = sqlite3.connect("herald.db")
    cur = con.cursor()
    while True:
        with cv:
            cv.wait()
        length = gq.qsize()
        for i in range(length):
            data = gq.get()
            if data == None:
                return
            match_data_list = data['data']['matches']
            leavers = stratz_remove_leavers(data)
            for m in match_data_list:
                if m['id'] not in leavers:
                    ids = get_steam_ids(m)
                    cur.executemany("insert or ignore into steam_ids values (?)",ids)
                    json_str = json.dumps(m)
                    cur.execute("INSERT OR IGNORE INTO match_info VALUES ('{}','{}','{}')".format(m['id'],datetime.utcfromtimestamp(m['startDateTime']).strftime('%Y-%m-%d %H:%M:%S'),json_str))
            con.commit()


# %%
json_data = query(days=3)
con = sqlite3.connect("herald.db")
cur = con.cursor()
matches = ([i['match_id'] for i in json_data['rows']])
cur.execute("SELECT matchId from match_info")
z = cur.fetchall()
parsed_ids = [d[0] for d in z]
s = [_id for _id in matches if _id not in parsed_ids]
threads = []
parsed_matches = []
print("Parsing {} Matches from the past 1 days".format(len(s)))
for i in tqdm.tqdm(range(0,len(s)-5,5)):
    worker_thread = threading.Thread(target=data_consumer_thread)
    worker_thread.start()
    parsed_matches.append(s[i:i+5])
    threads.append(threading.Thread(target = data_producer_thread, args = (s[i:i+5],)))
    if len(threads) == 10:
        for i in range(10):
            threads[i].start() 
        for i in range(10):
            threads[i].join() 
        threads = []
        parsed_matches = []
# %%

# %%
