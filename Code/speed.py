# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 08:21:46 2018

@author: user
"""

import numpy as np
import pandas as pd
import itertools
import re

#%%
gameId = 2017090700
min_yard = 7
min_yard_wr = 14
#%%
text = "https://raw.githubusercontent.com/nfl-football-ops/Big-Data-Bowl/master/Data/"

recordFile_name = 'tracking_gameId_' + str(gameId) + '.csv'
track_file = pd.read_csv(text + recordFile_name)

#game_file = pd.read_csv(text + 'games.csv')

plays_file = pd.read_csv(text + 'plays.csv')

player_file = pd.read_csv(text + 'players.csv')


#%%
# 1. Select players with positions Wide Receiver, Running Back, Corner Back, Safety
# 2. Plays with >= 10 yard distance and score increase with touchdown
# 3. Get players from playDescription

#%%
player_file2 = player_file.loc[player_file['PositionAbbr'].isin(['CB', 'SS', 'RB', 'WR']),]
main_file = track_file.merge(player_file2)
main_file = main_file.merge(plays_file)

#%%
main_file2 = main_file.groupby(['playId', 'nflId', 'PositionAbbr']).dis.sum().reset_index()
main_file21 = main_file2.loc[main_file2['dis'] >= min_yard, ]
main_file21 = main_file21.loc[~((main_file21['PositionAbbr'] == 'WR') 
    & (main_file21['dis'] < min_yard_wr)), ]

#%%
##%%
#plays_file2 = plays_file.loc[(plays_file[])]
##%%
#plays_file2 = plays_file.loc[((plays_file['gameId'] == gameId)
#    & (plays_file['PlayResult'] >= 10)), ]
#plays_file2 = plays_file2.loc[((plays_file2['HomeScoreBeforePlay'] < plays_file2['HomeScoreAfterPlay'])
#    | (plays_file2['VisitorScoreBeforePlay'] < plays_file2['VisitorScoreAfterPlay'])), ]
#
#track_file2 = track_file.groupby('playId').apply(lambda x: (x['event'] == 'touchdown').any())
#track_file2 = track_file2[track_file2 == True].index
#track_file2 = track_file.loc[track_file['playId'].isin(track_file2), ]
#
#main_file = track_file.merge(plays_file2, on=['gameId', 'playId'])
#
##%%
#
#pattern = r'(?:(?<=\.|\s)[A-Z]\.[A-Z][a-z]*)+'
#assoc_players = plays_file2.apply(lambda x: re.findall(pattern, x['playDescription']), axis=1)








