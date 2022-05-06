import requests
import pandas as pd

df = pd.DataFrame(columns = ['Name', 'Time On Ice', 'Assists', 'Goals', 'Shots'])

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
        link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x) + "/stats?stats=statsSingleSeason&season=20202021"
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
                goals = stat["goals"]
                toi = stat["timeOnIce"]
                assists = stat["assists"]
                shots = stat["goals"]
                new_row = {'Name':fullname, 'Time On Ice':toi, 'Assists':assists, 'Goals':goals, 'Shots':shots}
                df = df.append(new_row, ignore_index=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  
        print(df)
                
get_player_data(get_player_ids, df)