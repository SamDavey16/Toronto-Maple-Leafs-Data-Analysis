import requests
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
#from pandastable import Table, TableModel
def menu():
    df = pd.DataFrame(columns = ['Name', 'Games Played', 'Time On Ice', 'Assists', 'Goals', 'Shots', 'Rank'])

    goalie_df = pd.DataFrame(columns = ['Name', 'Games Played', 'Power Play Saves', 'Shots Against', 'Goals Against', 'Rank'])

    individual_df = pd.DataFrame(columns = ['Name', 'Games Played', 'Time On Ice', 'Assists', 'Goals', 'Shots'])

    root = tk.Tk()
    root.title("Player Data")
    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Players')
    tabControl.add(tab2, text='Goalies')
    tabControl.pack(expand=1, fill="both")
    
    def open_window():
        newWindow = Toplevel(root)
        newWindow.title("Goalie data")
        clear_data()
        tv1["column"] = list(goalie_df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 

        df_rows = goalie_df.to_numpy().tolist() 
        for row in df_rows:
            tv1.insert("", "end", values=row) 

    btn = Button(root,
             text ="Click to open a new window",
             command = open_window)
    btn.pack(pady = 10)
    btn.place(x=770, y=350)  

    root.geometry("1000x1000")
    root.pack_propagate(False) 
    root.resizable(0, 0) 

    frame1 = tk.LabelFrame(root, text="Player Data")
    frame1.place(height=500, width=500)

    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1) 

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) 
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) 
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    treescrollx.pack(side="bottom", fill="x") 
    treescrolly.pack(side="right", fill="y") 

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
                goalie_list.append(ids)
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

    def individual_player_data(get_player_ids, individual_df, get_goalie_ids):
        n = input("Enter player name: ")
        for x in get_player_ids():
            link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x) + "/stats?stats=statsSingleSeason&season=20212022"
            name_link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x)
            name_link = requests.get(name_link)
            name_link = name_link.json()
            people = name_link["people"]
            for l in people:
                fullname = l["fullName"]
            if fullname != n:
                continue
            else:
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
                        new_row = {'Name':fullname, 'Games Played':games_played, 'Time On Ice':toi, 'Assists':assists, 'Goals':goals, 'Shots':shots}
                        individual_df = individual_df.append(new_row, ignore_index=True)
                        #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(individual_df)

    def get_player_data(get_player_ids, df, get_goalie_ids, goalie_df):
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
        for x in get_goalie_ids():
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
                    stats2 = i["stat"]
                    pp_saves = int(stats2["powerPlaySaves"])
                    games = int(stats2["games"])
                    shots_against = int(stats2["shotsAgainst"])
                    goals_against = int(stats2["goalsAgainst"])
                    shutouts = int(stats2["shutouts"])
                    pps_percentage = float(stats2["powerPlaySavePercentage"])
                    shs_percentage = float(stats2["shortHandedSavePercentage"])
                    ess_percentage = float(stats2["evenStrengthSavePercentage"])
                    try:
                        ranks = games / pps_percentage + shs_percentage + ess_percentage + games
                    except:
                        ranks = 0
                    new_row = {'Name':fullname, 'Games Played':games, 'Power Play Saves':pp_saves, 'Shots Against':shots_against, 'Goals Against':goals_against, 'Rank':ranks}
                    goalie_df = goalie_df.append(new_row, ignore_index=True)
                    

        clear_data()
        tv1["column"] = list(df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 

        df_rows = df.to_numpy().tolist() 
        for row in df_rows:
            tv1.insert("", "end", values=row) 
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            goalie_df = goalie_df.sort_values(by=['Rank'], ascending=False)
            print(goalie_df)
            
    def clear_data():
        tv1.delete(*tv1.get_children())
        return None

    get_player_data(get_player_ids, df, get_goalie_ids, goalie_df)
    individual_player_data(get_player_ids, individual_df, get_goalie_ids)
    root.mainloop()

menu()