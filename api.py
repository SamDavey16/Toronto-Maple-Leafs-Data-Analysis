import requests
import pandas as pd
import tkinter as tk
from tkinter import *
from pandastable import Table, TableModel

df = pd.DataFrame(columns = ['Name', 'Games Played', 'Time On Ice', 'Assists', 'Goals', 'Shots', 'Rank'])

def get_goalie_ids():
    url = "https://statsapi.web.nhl.com/api/v1/teams/10/roster"
    url = requests.get(url)
    url = url.json()
    roster = url["roster"]
    goalie_list = []
    for i in roster:
        person = i["person"]
        position = i["position"]
        name = person["fullName"]
        ids = person["id"]
        if position["abbreviation"] == "G":
            id_list.append(ids)
    return goalie_list

def get_player_ids():
    url = "https://statsapi.web.nhl.com/api/v1/teams/10/roster"
    url = requests.get(url)
    url = url.json()
    roster = url["roster"]
    id_list = []
    for i in roster:
        person = i["person"]
        position = i["position"]
        name = person["fullName"]
        ids = person["id"]
        if position["abbreviation"] != "G":
            id_list.append(ids)
    return id_list

def get_player_data(get_player_ids, df):
    for x in get_player_ids():
        link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x) + "/stats?stats=statsSingleSeason&season=20212022"
        name_link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x)
        name_link = requests.get(name_link)
        name_link = name_link.json()
        people = name_link["people"]
        for l in people:
            fullname = l["fullName"]
        link = requests.get(link)
        link = link.json()
        stats = link["stats"]
        for i in stats:
            splits = i["splits"]
            for i in splits:
                stat = i["stat"]
                goals = int(stat["goals"])
                toi = stat["timeOnIce"]
                time = ''.join(x for x in toi if x.isdigit())
                time = int(time[:-2])
                assists = int(stat["assists"])
                shots = int(stat["shots"])
                games_played = int(stat["games"])
                try:
                    rank = games_played / goals + shots + assists
                except: # exception for the division by zero error for when there's no stats
                    rank = 0
                new_row = {'Name':fullname, 'Games Played':games_played, 'Time On Ice':toi, 'Assists':assists, 'Goals':goals, 'Shots':shots, 'Rank':rank}
                df = df.append(new_row, ignore_index=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        df = df.sort_values(by=['Rank'], ascending=False)
        print(df)
        


                
get_player_data(get_player_ids, df)