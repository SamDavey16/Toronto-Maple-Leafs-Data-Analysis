import matplotlib.pyplot as plt
import requests
from matplotlib import image
from hockey_rink import NHLRink
from PIL import Image
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import seaborn as sns

fig=plt.figure(figsize=(10,10))
plt.xlim([0,100])
plt.ylim([-42.5, 42.5])
Austonx = []
Austony = []

seasons = ["20212022"]
inname = input("Enter name: ")
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
                            print(n)
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