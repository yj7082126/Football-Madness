# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 14:33:25 2018

@author: user
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os
import re    

path = 'C:\\Users\\user\\Documents\\Big-Data-Bowl\\Data'

files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and 'tracking' in i]

#%% Parameters
min_yard = 7
min_yard_wr = 14

#%% Load Initial Files
text = "https://raw.githubusercontent.com/nfl-football-ops/Big-Data-Bowl/master/Data/"

game_file = pd.read_csv(text + 'games.csv')

plays_file = pd.read_csv(text + 'plays.csv')

player_file = pd.read_csv(text + 'players.csv')

df = pd.DataFrame(columns = ['gameId', 'playId', 'nflId', 'displayName', 'PositionAbbr', 'max_speed',
       'max_index', 'avg_speed'])
#%% plays_file2: list of plyaers that are associated with playDescription (key players)
pattern = r'(?:[A-Z]\.[A-Z][a-z]*)+'
plays_file['assoc_players'] = plays_file.apply(lambda x: 
    re.findall(pattern, x['playDescription']), axis=1)
plays_file2 = plays_file[['gameId', 'playId', 'assoc_players']]

assoc_players = 'assoc_players'
plays_file2 = pd.DataFrame({
    col:np.repeat(plays_file2[col].values, plays_file2['assoc_players'].str.len()) 
    for col in plays_file2.columns.difference(['assoc_players'])}).assign(
    **{assoc_players:np.concatenate(plays_file2['assoc_players'].values)})[
        plays_file2.columns.tolist()]
    
plays_file2['first'] = plays_file2['assoc_players'].apply(lambda x: x.split('.')[0]) 
plays_file2['last'] = plays_file2['assoc_players'].apply(lambda x: x.split('.')[1])

#%% function that calculates speed
def top_speed(tmp):
    df = pd.DataFrame(columns = ['max_speed'])
    for index, row in tmp.iterrows():
        if row['frame.id'] <= (tmp['frame.id'].max()-9):
            df.loc[row['frame.id']] = tmp.loc[index:index+10, 's'].mean()
    
    d = pd.Series()
    if (df['max_speed'].isnull().sum()) == 0:
        d['max_speed'] = round(df['max_speed'].max(), 2)
        d['max_index'] = df['max_speed'].idxmax()
    else:
        d['max_speed'] = 0.0
        d['max_index'] = 0.0
    d['avg_speed'] = (tmp['dis'].sum()/(tmp['frame.id'].max()-1))*10
    return d

#%% link plays_file2 with track_file
for recordFile_name in files:
    print(recordFile_name)
    track_file = pd.read_csv(text + recordFile_name)
    gameId = int(recordFile_name.split('.')[0].split('_')[2])

    tmp = plays_file2.loc[plays_file2['gameId'] == gameId, ]
    track_file['first'] = track_file['displayName'].apply(lambda x: x[0])
    track_file['last'] = track_file['displayName'].apply(lambda x: x.split(' ')[-1])
    track_file = track_file.merge(tmp, on=['gameId', 'playId', 'first', 'last'])
    track_file = track_file[['time', 'x', 'y', 's', 'dis', 'dir', 'event', 'nflId', 'displayName',
           'jerseyNumber', 'team', 'frame.id', 'gameId', 'playId']]

#%% get info of certain positions with valid distance limit, apply top_speed
    main_file = track_file.merge(player_file)
    main_file2 = main_file.loc[main_file['PositionAbbr'].isin(['CB', 'SS', 'RB', 'WR']),]
    
    main_file3 = main_file2.groupby(['playId', 'nflId', 'PositionAbbr']).dis.sum().reset_index()
    main_file31 = main_file3.loc[main_file3['dis'] >= min_yard, ]
    if len(main_file31) > 0:
        main_file31 = main_file31.loc[~((main_file31['PositionAbbr'] == 'WR') 
            & (main_file31['dis'] < min_yard_wr)), ]
    main_file31.columns = ['playId', 'nflId', 'PositionAbbr', 'sumdis']
    
    main_file = main_file2.merge(main_file31)

    main_fileX = main_file.groupby(['gameId', 'playId', 'nflId', 'displayName', 'PositionAbbr']
        ).apply(top_speed).reset_index()
    
    df = pd.concat([df, main_fileX])
