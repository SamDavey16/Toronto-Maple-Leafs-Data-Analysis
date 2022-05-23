import requests
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pandasgui import show
import matplotlib.pyplot as plt
import requests
from matplotlib import image
from hockey_rink import NHLRink
from PIL import ImageTk, Image
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import seaborn as sns
#if there is a module error for win32api run: pip install pypiwin32

def heat_map(inname):
    fig=plt.figure(figsize=(10,10))
    plt.xlim([0,100])
    plt.ylim([-42.5, 42.5])
    Austonx = []
    Austony = []

    seasons = ["20212022"]
    print("Loading heat map...")
    for season in seasons:
        tor_schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?season="+season+"&teamId=10&gameType=R")
        schedule = tor_schedule.json()
        schedule = schedule["dates"]

        game_ids=[]
        for game in schedule:
            game_data=game["games"]
            game_data=(game_data[0])
            status = game_data["status"]
            status = status["abstractGameState"]
            if status == "Preview":
                continue
            else:
                id = game_data["gamePk"]
                game_ids.append(id)

        for ids in game_ids:
            url = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(ids) + "/feed/live")
            content = url.json()

            event = content["liveData"]
            plays = event["plays"]
            all_plays = plays["allPlays"]
            for i in all_plays:
                result = i["result"]
                event = result["event"]
                if event=="Goal" or event == "Shot" or event=="Missed Shot":
                    team_info = i["team"]
                    team = team_info["triCode"]
                    players = i["players"]
                    for m in players:
                        playertype = m["playerType"]
                        if playertype == "Scorer":
                            scorer = m["player"]
                            n = scorer["fullName"]
                            if n == inname:
                                coord = (i["coordinates"])
                                x = int(coord["x"])
                                y = int(coord["y"])
                                if x < 0:
                                    x = abs(x)
                                    Austonx.append(x)
                                    y = y*-1
                                    Austony.append(y)

                                else:
                                    x=x
                                    Austonx.append(x)
                                    y=y
                                    Austony.append(y)
                else:
                    continue
                
    rink = NHLRink()
    ax = rink.draw(display_range="ozone")
    hb = ax.hexbin(Austonx, Austony, gridsize=25, cmap='Reds')
    ax.clear()
    ax = rink.draw(display_range="ozone")
    cb = fig.colorbar(hb, ax=ax, label='Goal Frequency')
    kde = sns.kdeplot(
        Austonx,Austony, shade = True, shade_lowest = False, alpha=1, cmap="Reds"
    )


    plt.title(inname + " Goals: 2021-2022")
    plt.show()

def menu():
    df = pd.DataFrame(columns = ['Name', 'Games Played', 'Time On Ice', 'Assists', 'Goals', 'Shots', 'Rank'])

    goalie_df = pd.DataFrame(columns = ['Name', 'Games Played', 'Power Play Saves', 'Shots Against', 'Goals Against', 'Rank'])

    individual_df = pd.DataFrame(columns = ['Name', 'Games Played', 'Time On Ice', 'Assists', 'Goals', 'Shots'])

    root = tk.Tk()
    root.title("Player Data")
    
    root.geometry("800x800")
    root.pack_propagate(False) 
    root.resizable(0, 0) 

    def goal_rank(goal_list, goal, name):
        goal_list.sort()
        i = 0
        for l in goal_list:
            if l < goal:
                i += 1
            else:
                percentile = i / len(goal_list) * 100
        pos = len(goal_list) - i
        print(name, "is #", pos, "for goals with a percentile rank of:", percentile)

    def assist_rank(assist_list, assists, name):
        assist_list.sort()
        i = 0
        for l in assist_list:
            if l < assists:
                i += 1
            else:
                percentile2 = i / len(assist_list) * 100
        pos = len(assist_list) - i
        print(name, "is #", pos, "for assists with a percentile rank of:", percentile2)

    def shot_rank(shot_list, shots, name):
        shot_list.sort()
        i = 0
        percent = 0
        for l in shot_list:
            if l < shots:
                i += 1
            else:
                percent = i / len(shot_list) * 100
        pos = len(shot_list) - i
        print(name, "is #", pos, "for shots with a percentile rank of:", percent)

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
        goal_list = []
        shot_list = []
        assist_list = []
        for x in get_player_ids():
            link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x) + "/stats?stats=statsSingleSeason&season=20212022"
            name_link = "https://statsapi.web.nhl.com/api/v1/people/" + str(x)
            name_link = requests.get(name_link)
            name_link = name_link.json()
            people = name_link["people"]
            for l in people:
                fullname = l["fullName"]
            if fullname != n:
                link = requests.get(link)
                link = link.json()
                stats = link["stats"]
                for i in stats:
                    splits = i["splits"]
                    for i in splits:
                        stat = i["stat"]
                        goals = int(stat["goals"])
                        goal_list.append(goals)
                        assists = int(stat["assists"])
                        assist_list.append(assists)
                        shots = int(stat["shots"])
                        shot_list.append(shots)
                continue
            else:
                link = requests.get(link)
                link = link.json()
                stats = link["stats"]
                for i in stats:
                    splits = i["splits"]
                    for i in splits:
                        stat = i["stat"]
                        goal = int(stat["goals"])
                        goal_list.append(goal)
                        toi = stat["timeOnIce"]
                        time = ''.join(x for x in toi if x.isdigit())
                        time = int(time[:-2])
                        assist = int(stat["assists"])
                        assist_list.append(assist)
                        shot = int(stat["shots"])
                        shot_list.append(shot)
                        games_played = int(stat["games"])
                        new_row = {'Name':fullname, 'Games Played':games_played, 'Time On Ice':toi, 'Assists':assist, 'Goals':goal, 'Shots':shot}
                        individual_df = individual_df.append(new_row, ignore_index=True)
        show(individual_df)
        heat_map(n)
        goal_rank(goal_list, goal, n)
        assist_rank(assist_list, assist, n)
        shot_rank(shot_list, shot, n)


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
                        rank = 23 / goals + shots + assists
                    except: # exception for the division by zero error for when there's no stats
                        rank = 0
                    new_row = {'Name':fullname, 'Games Played':games_played, 'Time On Ice':toi, 'Assists':assists, 'Goals':goals, 'Shots':shots, 'Rank':rank}
                    df = df.append(new_row, ignore_index=True)
        return df
    
    def get_goalie_data(get_goalie_ids, goalie_df):
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
                        ranks = 23 / pps_percentage + shs_percentage + ess_percentage + games
                    except:
                        ranks = 0
                    new_row = {'Name':fullname, 'Games Played':games, 'Power Play Saves':pp_saves, 'Shots Against':shots_against, 'Goals Against':goals_against, 'Rank':ranks}
                    goalie_df = goalie_df.append(new_row, ignore_index=True)
        show(goalie_df)
                    
    df = get_player_data(get_player_ids, df)
    #goalie_df = get_goalie_data(get_goalie_ids, goalie_df)

    t = Label(root, text = "NHL Player Analysis", font = "Helvetica 12 bold", bg="white")
    t.pack()
    t2 = Label(root, text = "", bg = "white")
    t2.pack()
    t3 = Label(root, text = "All data is stored in pandas dataframes. Select either to analyse a roster or an individual player.", font = "Helvetica 12 bold", bg = "white")
    t3.pack()

    btn = Button(root,
             text ="Analyse individual player data",
             command = lambda : individual_player_data(get_player_ids, individual_df, get_goalie_ids))
    btn.pack(pady = 10)
    btn.place(x=450, y=350)  

    btn2 = Button(root,
             text ="Analyse player roster data",
             command = lambda : show(df))
    btn2.pack(pady = 10)
    btn2.place(x=450, y=300)

    btn3 = Button(root,
             text ="Analyse goalie roster data",
             command = lambda : get_goalie_data(get_goalie_ids, goalie_df))
    btn3.pack(pady = 10)
    btn3.place(x=450, y=400)

    frame = Frame(root, width=300, height=200)
    frame.pack()
    frame.place(anchor='center', relx=0.2, rely=0.8)

    img = Image.open("NHL-Logo.png")
    img = img.resize((300, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    pic = Label(frame, image = img)
    pic.pack()

    root.mainloop()

menu()