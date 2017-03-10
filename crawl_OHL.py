import HTMLParser
from bs4 import BeautifulSoup
import urllib
import re
import json
from pprint import pprint
from collections import OrderedDict
import pandas as pd
import re
import numpy as np
import csv

def get_path(dct, path):
    for i, p in re.findall(r'(\d+)|(\w+)', path):
        dct = dct[p or int(i)]
    return dct

row=[]
result = []
games_id=[]
games_date_played=[]
games_goals=[]
games_points=[]
games_assists=[]
games_pim=[]
games_plus_minus=[]

for  num in range(6888,6900):
    urls=[]
    url="http://cluster.leaguestat.com/feed/?feed=modulekit&view=player&key=c680916776709578&fmt=json&client_code=ohl&lang=en&player_id="+str(num)+"&category=gamebygame"
    handle=urllib.urlopen(url)
    html_gunk=handle.read()
    soup=BeautifulSoup(html_gunk)
    #print soup.prettify
    test=soup.p.string
    res=json.loads(test.decode('utf-8'))
    #pprint(res)
    #data = json.loads(test, object_pairs_hook=OrderedDict)
    #print(json.dumps(data, indent=4))
    #print data.values()[0]
    #print res.values()
    #df = pd.io.json.json_normalize(res.values())
    #df.columns = df.columns.map(lambda x: x.split(".")[-1])
    try:
        season_info=get_path(res, "SiteKit.Player.seasons_played")
        season_id=[]
        season_name=[]
        for i in range(0,len(season_info)):
            season_id.append(season_info[i]['season_id'])
            season_name.append(season_info[i]['season_name'])
            
    except KeyError:
        season_id.append("")
        season_name.append("")
        continue
    player_id=res['SiteKit']['Parameters']['player_id']
    
    
    for season in season_id:
            urls.append("http://cluster.leaguestat.com/feed/?feed=modulekit&view=player&key=c680916776709578&fmt=json&client_code=ohl&lang=en&player_id="+str(num)+"&season_id="+str(season)+"&category=gamebygame"
         )
    for url in urls:
            handle=urllib.urlopen(url)
            html_gunk=handle.read()
            soup=BeautifulSoup(html_gunk)
            #print soup.prettify
            test=soup.p.string
            res=json.loads(test.decode('utf-8'))
           
            try:
                g=get_path(res, "SiteKit.Player.games")
            except KeyError:
                continue
            for i in range(0,len(g)):
                try:
                  games_id.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".id"))
                except KeyError:
                  game_id.append("")
                try:
                  games_date_played.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".date_played"))
                except KeyError:
                  games_date_played.append("")
                try:
                  games_goals.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".goals"))
                except KeyError:
                  games_goals.append("")
                try:
                  games_points.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".points"))
                except KeyError:
                  games_points.append("")
                try:
                  games_assists.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".assists"))
                except KeyError:
                  games_assists.append("")
                try:
                  games_plus_minus.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".plusminus"))
                except KeyError:
                  games_plus_minus.append("")
                try:
                  games_pim.append(get_path(res, "SiteKit.Player.games["+str(i)+"]"+".penalty_minutes"))
                except KeyError:
                  games_pim.append("")  
            
    player=[]    
    for p in range(0,len(games_id)):
        player.append(player_id)
    result.append(np.column_stack((player,games_id,games_date_played,games_goals,games_points,games_assists,games_plus_minus,games_pim)))

myfile=open('/Users/YejiaLiu/Downloads/myfile.csv','wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(['playerId','gameId','date','goals','points','assists','plusMinus','PIM'])
for i in range(0,len(result)):
    for j in range(0,len(result[i])):
        wr.writerow(result[i][j])







