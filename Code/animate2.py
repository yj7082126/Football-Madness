# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:12:25 2018

@author: user
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import itertools
import re
plt.rcParams[
    'animation.ffmpeg_path'] = 'C:\\Users\\user\\Downloads\\setup\\ffmpeg\\ffmpeg\\bin\\ffmpeg'
        

#%%
gameId = 2017090700

text = "https://raw.githubusercontent.com/nfl-football-ops/Big-Data-Bowl/master/Data/"

recordFile_name = 'tracking_gameId_' + str(gameId) + '.csv'
track_file = pd.read_csv(text + recordFile_name)

game_file = pd.read_csv(text + 'games.csv')

plays_file = pd.read_csv(text + 'plays.csv')

mFile = track_file.merge(game_file)
mFile = mFile.merge(plays_file)

xmin = 0
xmax = (160/3)
hash_right = 38.35
hash_left = 12
hash_width = 3.3

ymin=0
ymax=120

xlim = [0, (701/30), (899/30), xmax]
ylim = list(range(10, 110))

df_hash = pd.DataFrame(list(itertools.product(xlim,ylim)))
df_hash.columns = ['x', 'y']

df_hash = df_hash.loc[(df_hash['y'] % 5) != 0, ]

def update(frame):
    frame_file = main_file.loc[main_file['frame.id'] == frame, ]
    
    players.set_offsets(np.c_[xmax-frame_file['y'], frame_file['x']])
    players.set_color(frame_file['team'].apply(lambda x: color[x]))
    
    for el in numbers:
        row = frame_file.loc[frame_file['jerseyNumber'] == int(el.get_text()), ]
        el.set_position((xmax-row['y'], row['x']))
        el.set_color('white')
    
    if frame in list(actions['frame.id']):
        action.set_text(actions.loc[actions['frame.id'] == frame, 'event'].iloc[0])
    
    return players, numbers, action


#%%
plays = list(track_file['playId'].drop_duplicates())
for playId in plays:
    main_file = mFile.loc[mFile['playId'] == playId, ]

    home_team = main_file['homeDisplayName'].iloc[0]
    visitor_team = main_file['visitorDisplayName'].iloc[0]
    title = home_team + ' v. ' + visitor_team + ' (' + str(playId) + ')'
    
    game_date = main_file['gameDate'].iloc[0]
    game_time = main_file['gameTimeEastern'].iloc[0]
    game_stadium = main_file['Stadium'].iloc[0]
    game_location = main_file['Location'].iloc[0]
    
    subtitle = 'Time: ' + str(game_date) + ' ' + str(game_time) + '\nStadium: ' + str(
            game_stadium) + ' ' + str(game_location)
    
    actions = main_file.loc[~main_file['event'].isna(), ]
    
    commentary = str(main_file["playDescription"].iloc[0])
    commentary = re.sub("(.{48})", "\\1\n", commentary, 0, re.DOTALL)
#    play_text = "Play ID: " + str(main_file['playId'].iloc[0]) + "\nQuarter: " + str(main_file[
#            'quarter'].iloc[0]) + " Clock: " + str(main_file['GameClock'].iloc[0
#            ]) + "\nScore: " + str(main_file['HomeScoreBeforePlay'].iloc[0]) + ":" + str(main_file[
#            'VisitorScoreBeforePlay'].iloc[0]) + " --> " + str(main_file["HomeScoreAfterPlay"
#            ].iloc[0]) + ":" + str(main_file["VisitorScoreAfterPlay"].iloc[0]) + "\nCommentary: " + str(
#            " ".join(commentary.split(' ')[:2])) + "\n" + " ".join(commentary.split(' ')[2:
#            ]).split(',')[0] + "\n" + " ".join(commentary.split(' ')[2:]).split(',')[1]
 
    play_text = "Play ID: " + str(main_file['playId'].iloc[0]) + "\nQuarter: " + str(main_file[
            'quarter'].iloc[0]) + " Clock: " + str(main_file['GameClock'].iloc[0
            ]) + "\nScore: " + str(main_file['HomeScoreBeforePlay'].iloc[0]) + ":" + str(main_file[
            'VisitorScoreBeforePlay'].iloc[0]) + " --> " + str(main_file["HomeScoreAfterPlay"
            ].iloc[0]) + ":" + str(main_file["VisitorScoreAfterPlay"].iloc[0]) + "\nCommentary: " + str(
            commentary)
    
#%%
    color = {'home': 'blue', 'away': 'red', 'ball': 'black'}
    inv_size = 10
    el_size = 200
    play_loc = [60, 100]
    
    frame = 1
    fig, ax = plt.subplots(figsize=((xmax-xmin)/inv_size, (ymax-ymin)/inv_size))
    frame_file = main_file.loc[main_file['frame.id'] == frame, ]
    
    players = ax.scatter(x = xmax-frame_file['y'], y = frame_file['x'], 
               c = frame_file['team'].apply(lambda x: color[x]), s = el_size)
     
    numbers = []
    for index, row in frame_file.iterrows():
        if ~(np.isnan(row['jerseyNumber'])):
            numbers.append(ax.text(xmax-row['y'], row['x'], int(row['jerseyNumber']), 
                    weight='bold', color='white', horizontalalignment='center',
                    verticalalignment='center'))
               
            
    label_list = ["G"] + list(range(10, 60, 10)) + list(range(40, 0, -10)) + ["G"]
    for i, label in enumerate(label_list):
        ax.text(x = 12, y = 10*(i+1), s = label, 
                horizontalalignment='center',
                verticalalignment='center', rotation=270)
        ax.text(x = xmax - 12, y = 10*(i+1), s = label, 
                horizontalalignment='center',
                verticalalignment='center', rotation=90)
    
    for index, row in df_hash.iterrows():
        if (row['x'] < 27.5):
            ax.text(row['x'], row['y'], '_', 
                    horizontalalignment='left',
                    verticalalignment='bottom')
        else:
            ax.text(row['x'], row['y'], '_', 
                    horizontalalignment='right',
                    verticalalignment='bottom')
    
    if frame in list(actions['frame.id']):
        action = ax.text(x = xmax/2, y = 0, s = actions.loc[actions['frame.id'] == frame, 
             'event'].iloc[0], horizontalalignment='center', verticalalignment='top')
    else:
        action = ax.text(x = xmax/2, y = 0, s = "", 
            horizontalalignment='center', verticalalignment='top') 
                
    ax.set_title(title + '\n' + subtitle + '\n' + play_text)
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    for i in list(range(10, 115, 10)):
        plt.axhline(y=i, linewidth=1, color='black')
    for i in list(range(10, 115, 5)):
        plt.axhline(y=i, linewidth=0.5, color='black')    
        
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    #plt.tight_layout()
    plt.show()

#%%
    an = ani.FuncAnimation(fig, update, frames=list(range(1, max(main_file['frame.id'])+1)))
    
    Writer = ani.writers['ffmpeg']
    writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    
    video_title = str(gameId) + '_' + str(playId) + '.mp4'
    an.save(video_title,  writer=writer)
    print(playId)