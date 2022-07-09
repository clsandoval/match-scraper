#%%
import urllib 
import pypika
import json
import requests
import time
from urllib import parse 
from datetime import datetime, timedelta
from pypika import Query,Table
from pypika import functions as fn
from config import *
from env import STRATZ_API_TOKEN
from data import *


def stratz_remove_leavers(data):
    match_ids = set()
    match_data = data['data']['matches']
    for match in match_data:
        match_id = match['id']
        player_data = match['players']
        for player in player_data:
            if player['leaverStatus'] == 'DISCONNECTED_TOO_LONG' or player['leaverStatus'] == 'ABANDONED' or player['leaverStatus'] == 'AFK':
                match_ids.add(match_id)
    return match_ids


def query_matches_window(matches, url = STRATZ_GRAPHQL_URL,start_query=start_graphql_query,end_query=new_end_graphql_query, api_token=STRATZ_API_TOKEN):
    headers = {"Authorization": f"Bearer {api_token}"}
    url =url
    query = start_query
    for m in matches:
        query += "{},".format(m)
    query +=end_query
    while True:
        try:
            r = requests.post(url, json={"query":query}, headers=headers)
            break
        except:
            time.sleep(5)
    data = json.loads(r.text) 
    return data


def query_matches(matches, url = STRATZ_GRAPHQL_URL,start_query=start_graphql_query,end_query=end_graphql_query, api_token=STRATZ_API_TOKEN):
    headers = {"Authorization": f"Bearer {api_token}"}
    url =url
    query = start_query
    for m in matches:
        query += "{},".format(m)
    query +=end_query
    while True:
        try:
            r = requests.post(url, json={"query":query}, headers=headers)
            break
        except:
            time.sleep(5)
    data = json.loads(r.text) 
    return data


def query_players(ids, url = STRATZ_GRAPHQL_URL, start_query=player_specific_graphql_query, end_query=player_specific_graphql_query_end, api_token=STRATZ_API_TOKEN):
    headers = {"Authorization": f"Bearer {api_token}"}
    url =url
    query = start_query
    for d in ids:
        query += "{},".format(d)
    query +=end_query
    while True:
        try:
            r = requests.post(url, json={"query":query}, headers=headers)
            break
        except:
            time.sleep(5)
    data = json.loads(r.text) 
    return data


def query(url=OPENDOTA_URL,days = 1):
    public_matches = Table('public_matches')
    d_t = (datetime.now()-timedelta(days=days)).timestamp()
    base_sql = "explorer?sql="
    q = Query.from_(public_matches).select(
        public_matches.match_id, public_matches.start_time, public_matches.avg_rank_tier
    ).where(
        public_matches.start_time >= d_t
    ).where(
        public_matches.avg_rank_tier <=16
    )
    request = url +base_sql+ parse.quote(str(q))
    print(request)
    req = urllib.request.Request(url = request, headers = QUERY_HEADER)
    while True:
        try:
            data = urllib.request.urlopen(req)
            break
        except:
            print("Timeout, retrying in 10 seconds")
            time.sleep(10)
    json_data = json.loads(data.read())
    return json_data


def get_items(player):
    return player['item0Id'],player['item1Id'], player['item2Id'], player['item3Id'], player['item4Id'], player['item5Id']


def get_num_items(items):
    d = {}
    for key,value in item_dict.items():
        n = 0
        for i in items:
            if i == value:
                n+=1
        d[key] = n
    return d


def construct_dict(top):
    max_dict={
        "maxDuration":[[0,0] for i in range(top)],
        "minDuration":[[999999,0] for i in range(top)],
        "maxKills":[[0,0] for i in range(top)],
        "maxDeaths":[[0,0] for i in range(top)],
        "dotaPlus":[[0,0,0,0]],
        "dotaPlusMultiple":[[0,0,0,0]],
    }
    for key,value in item_dict.items():
        max_dict[key] = [[0,0,''] for i in range(top)]
    return max_dict


def construct_player_dict(top):
    max_dict={
        "minBehaviourScore":[[10000] for i in range(top)],
        "matchCount":[[0] for i in range(top)],
    }
    for key,value in hero_dict.items():
        max_dict[key] = {
            "longestStreak":[[0] for i in range(top)],
            "currentStreak":[[0] for i in range(top)],
            "matchCount":[[0] for i in range(top)],
            "kDA":[[0] for i in range(top)],
            "duration":[[0] for i in range(top)]
        }
    return max_dict




def get_matches_maxmin(d,match,double_racks_down,match_duration,match_id,match_rank,top):
    if match_duration != None:
        i = 0
        while True:
            if i > top-1:
                break
            if match_duration > d['maxDuration'][i][0]:
                d['maxDuration'].insert(i,[match_duration,match_id,match_rank])
                if len(d['maxDuration'])> top:
                    d['maxDuration'] = d['maxDuration'][:-1]
                break
            i+=1
        i = 0
        while True:
            if i  > top-1:
                break
            if match_duration < d['minDuration'][i][0] and match_duration > 0 and (match['analysisOutcome'] != 'STOMPED' ) and (match['analysisOutcome'] != 'NONE' ) and double_racks_down:
                d['minDuration'].insert(i,[match_duration,match_id,match_rank])
                if len(d['minDuration'])> top:
                    d['minDuration'] = d['minDuration'][:-1]
                break
            i+=1
    return d


def get_matchstats(match):
        radiant_racks = match['barracksStatusRadiant']
        dire_racks = match['barracksStatusDire']
        match_duration = match['durationSeconds']
        match_rank = match['actualRank']
        match_id = match['id']
        double_racks_down = False
        if radiant_racks !=63 and dire_racks != 63:
            double_racks_down = True
        return radiant_racks, dire_racks, match_duration, match_rank, match_id, double_racks_down


def get_max_items(max_dict,match_item_dict,top, match_id,match_rank,match_duration):
    for key,value in match_item_dict.items():
        i = 0
        while True:
            if i > top-1:
                break
            if value > max_dict[key][i][0]:
                max_dict[key].insert(i,[value,match_id,match_rank,match_duration])
                if len(max_dict[key])>top:
                    max_dict[key] = max_dict[key][:-1]
                break
            i+=1
    return max_dict


def get_max_deaths(max_dict,deaths,top, match_id,match_rank,match_duration):
    i = 0
    while True:
        if  i > top-1:
            break
        if deaths > max_dict['maxDeaths'][i][0]:
            max_dict['maxDeaths'].insert(i,[deaths,match_duration,match_id,match_rank])
            if len(max_dict['maxDeaths'])> top:
                max_dict['maxDeaths'] = max_dict['maxDeaths'][:-1]
            break
        i+=1
    return max_dict


def get_max_kills(max_dict,max_kills,top, match_id,match_rank,match_duration):
    i = 0
    while True:
        if  i > top-1:
            break
        if max_kills > max_dict['maxKills'][i][0]:
            max_dict['maxKills'].insert(i,[max_kills,match_duration,match_id,match_rank])
            if len(max_dict['maxKills'])> top:
                max_dict['maxKills'] = max_dict['maxKills'][:-1]
            break
        i+=1
    return max_dict


def check_five_stack(match):
    player_data = match['players']
    fdict = {}
    for player in player_data:
        if player['partyId'] != None:
            if player['partyId'] in fdict:
                fdict[player['partyId']] +=1
            else:
                fdict[player['partyId']] = 1
    for key,value in fdict.items():
        if value != 5:
            return False
    if len(fdict.keys())!=2:
        return False
    return True


def get_steam_ids(m):
    ids = []
    player_data = m['players']
    for player in player_data:
        ids.append((int(player['steamAccountId']),))
    return ids


def get_maximums_per_player(match_data,top=5,five_stacks=False):
    max_dict=construct_dict(top)
    for match in match_data:
        if "lobbyType" not in match:
            continue
        if match['lobbyType'] != "RANKED":
            continue
        if five_stacks:
            if not check_five_stack(match):
                continue
        radiant_racks, dire_racks, match_duration, match_rank, match_id, double_racks_down = get_matchstats(match)
        if int(match_rank) <20 and double_racks_down:
            max_dict = get_matches_maxmin(max_dict,match,double_racks_down,match_duration,match_id,match_rank,top)
            player_data = match['players']
            match_item_dict = {}
            match_kills = 0
            for player in player_data:
                hero_name = player['hero']['name']
                stats = player['stats']
                player_deaths = 0
                if stats['killCount']!= None:
                    match_kills += stats['killCount']
                if stats['deathCount']!= None:
                    player_deaths= stats['deathCount']
                if match_duration > 3500:
                    max_dict = get_max_deaths(max_dict,player_deaths,top,match_id,match_rank,match_duration)
                items = get_items(player)
                player_item_dict = get_num_items(items)
                if (player['dotaPlus']) != None:
                    if player['dotaPlus']['level'] == 30:
                        if max_dict['dotaPlus'][-1][1] == match_id:
                                max_dict['dotaPlusMultiple'].append([player['dotaPlus']['level'],match_id,match_duration,hero_name])
                        max_dict['dotaPlus'].append([player['dotaPlus']['level'],match_id,match_duration,hero_name])
                for key,value in player_item_dict.items():
                    if key in match_item_dict:
                        match_item_dict[key] += value
                    else:
                        match_item_dict[key] = value

            max_dict = get_max_kills(max_dict,match_kills,top,match_id,match_rank,match_duration)
            max_dict = get_max_items(max_dict,match_item_dict,top,match_id,match_rank,match_duration)
    return max_dict