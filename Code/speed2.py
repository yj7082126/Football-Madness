# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 10:17:07 2018

@author: user
"""

import pandas as pd
import os
path = 'C:\\Users\\user\\Documents\\Big-Data-Bowl\\Data'

files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'tracking' in i]

text = "https://raw.githubusercontent.com/nfl-football-ops/Big-Data-Bowl/master/Data/"


game_file = pd.read_csv(text + 'games.csv')

plays_file = pd.read_csv(text + 'plays.csv')

player_file = pd.read_csv(text + 'players.csv')

df = pd.DataFrame(columns = ['gameId', 'playId', 'nflId'])
#%%
for recordFile_name in files:
    print(recordFile_name)
    track_file = pd.read_csv(text + recordFile_name)
    gameId = int(files[0].split('.')[0].split('_')[2])
    
    plays_file2 = plays_file.loc[((plays_file['gameId'] == gameId)
        & (plays_file['PlayResult'] >= 10)), ]
    plays_file2 = plays_file2.loc[((plays_file2['HomeScoreBeforePlay'] < plays_file2['HomeScoreAfterPlay'])
        | (plays_file2['VisitorScoreBeforePlay'] < plays_file2['VisitorScoreAfterPlay'])), ]
    
    track_file2 = track_file.groupby('playId').apply(lambda x: (x['event'] == 'touchdown').any())
    track_file2 = track_file2[track_file2 == True].index
    track_file2 = track_file.loc[track_file['playId'].isin(track_file2), ]
    
    main_file = track_file.merge(plays_file2, on=['gameId', 'playId'])
    
    player_file2 = player_file.loc[player_file['PositionAbbr'].isin(['CB', 'SS', 'RB', 'WR'])]
    main_file = main_file.merge(player_file2)
    main_file = main_file[['gameId', 'playId', 'nflId']].drop_duplicates()
    df = pd.concat([df, main_file])

