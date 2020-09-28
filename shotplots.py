#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:42:08 2020

@author: ncalvertuk
"""

#import datetime as dt
#import json
import matplotlib.pyplot as plt
import numpy as np
#from os import listdir
#from os.path import isfile, join
#from os import walk
#import pandas as pd
#import re
#import requests
from scipy import stats
import seaborn as sns
#import time

# Define the team colours
teamcols = [
    "#148c99ff",
    "#cc0929ff",
    "#0a3369ff",
    "#032c54ff",
    "#f9cf37ff",
    "#614f9bff",
    "#91052eff",
    "#6f359eff",
    "#e6a437ff",
    "#fd8a25ff"
    ]



def plotshotmap(base_image,d1,d2,a,title):
    '''
    A function to plot a shot heat map superimposed on top the base
    image of the rink layout.

    Parameters
    ----------
    base_image : numpy.ndarray
        The image of the rink layout
    d1 : numpy.ndarray
        The x coordinates of the shots.
    d2 : numpy.ndarray
        The y coordinates of the shots.
    a : matplotlib.axes
        The axis to plot to.
    title : string
        The title of the plot.

    Returns
    -------
    None.

    '''
    a.imshow(base_image,extent = (-50,50,0,100))
    sns.kdeplot(
        data=d1,
        data2=d2,
        shade=True,
        ax=a,
        alpha=0.8,
        shade_lowest=False,
        cmap="Reds"
        )
    a.set_title(title)
    a.set_xlim(-50,50)
    a.set_ylim(0,100)
    a.set_xlabel('')
    a.set_ylabel('')
    a.set_xticks([])
    a.set_yticks([])
    
def plotrinkmaps(df,teamname,base_image):
    '''
    A function to generate shot heat maps for shots at a single rink/arena.
    5 x 3 plots are generated, the 3 columns relating to shots by the home
    team, away team, and both teams combined. The 5 rows relating to
    all shots, goals, saved shots, blocked shots, and wide shots

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team who play at the rink.
    base_image : numpy.ndarray
        The image of the rink layout

    Raises
    ------
    ValueError
        If an incorrect team name is specified.

    Returns
    -------
    None.

    '''
    if sum(df.loc[:,"team_name"] == teamname) < 1:
        raise ValueError('Incorrect team name specified.')
    f, axs = plt.subplots(5,3,figsize=(15, 15))
    i= -1
    home = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == True)
    )
    away = (
        (df.loc[:,"opposition_name"] == teamname) &
        (df.loc[:,"home_game"] == False)
    )
    x_h = df.loc[home,"coordinate_x"]
    y_h = df.loc[home,"coordinate_y"]
    x_a = df.loc[away,"coordinate_x"]
    y_a = df.loc[away,"coordinate_y"]
    x_ha = x_h.append(-x_a)
    y_ha = y_h.append(-y_a)
    plotshotmap(
        base_image,
        -0.5*y_h,
        x_h,axs[i+1,0],
        teamname+' Home Team All Shots (n=' + str(len(x_h)) + ")"
        )
    plotshotmap(
        base_image,
        0.5*y_a,
        -x_a,axs[i+1,1],
        teamname+' Away Team All Shots (n=' + str(len(x_a)) + ")"
        )
    plotshotmap(
        base_image,
        -0.5*y_ha,
        x_ha,axs[i+1,2],
        teamname+' Both Teams All Shots (n=' + str(len(x_ha)) + ")"
        )
    shot_types = ["goal","saved","blocked","wide"]
    for i in range(0,len(shot_types)):
        st = shot_types[i]
        home = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st)
        )
        away = (
            (df.loc[:,"opposition_name"] == teamname) &
            (df.loc[:,"home_game"] == False) &
            (df.loc[:,"shot_outcome"] == st)
        )
        x_h = df.loc[home,"coordinate_x"]
        y_h = df.loc[home,"coordinate_y"]
        x_a = df.loc[away,"coordinate_x"]
        y_a = df.loc[away,"coordinate_y"]
        x_ha = x_h.append(-x_a)
        y_ha = y_h.append(-y_a)
        plotshotmap(
            base_image,
            -0.5*y_h,
            x_h,axs[i+1,0],
            teamname+' Home Team ' + st +" (n=" + str(len(x_h)) + ")"
            )
        plotshotmap(
            base_image,
            0.5*y_a,
            -x_a,axs[i+1,1],
            teamname+' Away Team ' + st +" (n=" + str(len(x_a)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_ha,
            x_ha,axs[i+1,2],
            teamname+' Both Teams ' + st +" (n=" + str(len(x_ha)) + ")"
            )
    plt.tight_layout();
    
def plotteammaps(df,teamname,base_image):
    '''
    A function to generate shot heat maps for shots by a single team.
    5 x 3 plots are generated, the 3 columns relating to shots at home,
    away , and both combined. The 5 rows relating to all shots, goals,
    saved shots, blocked shots, and wide shots.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team to plot.
    base_image : numpy.ndarray
        The image of the rink layout

    Raises
    ------
    ValueError
        If an incorrect team name is specified.

    Returns
    -------
    None.

    '''
    if sum(df.loc[:,"team_name"] == teamname) < 1:
        raise ValueError('Incorrect team name specified.')
    f, axs = plt.subplots(5,3,figsize=(15, 15))
    i= -1
    home = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == True)
    )
    away = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == False)
    )
    x_h = df.loc[home,"coordinate_x"]
    y_h = df.loc[home,"coordinate_y"]
    x_a = df.loc[away,"coordinate_x"]
    y_a = df.loc[away,"coordinate_y"]
    x_ha = x_h.append(-x_a)
    y_ha = y_h.append(-y_a)
    plotshotmap(
        base_image,
        -0.5*y_h,
        x_h,axs[i+1,0],
        teamname+' Home All Shots (n=' + str(len(x_h)) + ")"
        )
    plotshotmap(
        base_image,
        0.5*y_a,
        -x_a,axs[i+1,1],
        teamname+' Away All Shots (n=' + str(len(x_a)) + ")"
        )
    plotshotmap(
        base_image,
        -0.5*y_ha,
        x_ha,axs[i+1,2],
        teamname+' H&A Teams All Shots (n=' + str(len(x_ha)) + ")"
        )
    shot_types = ["goal","saved","blocked","wide"]
    for i in range(0,len(shot_types)):
        st = shot_types[i]
        home = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st)
        )
        away = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == False) &
            (df.loc[:,"shot_outcome"] == st)
        )
        x_h = df.loc[home,"coordinate_x"]
        y_h = df.loc[home,"coordinate_y"]
        x_a = df.loc[away,"coordinate_x"]
        y_a = df.loc[away,"coordinate_y"]
        x_ha = x_h.append(-x_a)
        y_ha = y_h.append(-y_a)
        plotshotmap(
            base_image,
            -0.5*y_h,
            x_h,axs[i+1,0],
            teamname+' Home ' + st +" (n=" + str(len(x_h)) + ")"
            )
        plotshotmap(
            base_image,
            0.5*y_a,
            -x_a,axs[i+1,1],
            teamname+' Away ' + st +" (n=" + str(len(x_a)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_ha,
            x_ha,axs[i+1,2],
            teamname+' H&A ' + st +" (n=" + str(len(x_ha)) + ")"
            )
    plt.tight_layout();
    
def plotteamhomeperiodmaps(df,teamname,base_image):
    '''
    A function to generate shot heat maps for shots by a single team playing
    at home split into the 3 periods. 5 x 3 plots are generated, 
    the 3 columns relating to each period. The 5 rows relating to all shots,
    goals, saved shots, blocked shots, and wide shots

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team to plot.
    base_image : numpy.ndarray
        The image of the rink layout

    Raises
    ------
    ValueError
        If an incorrect team name is specified.

    Returns
    -------
    None.

    '''
    if sum(df.loc[:,"team_name"] == teamname) < 1:
        raise ValueError('Incorrect team name specified.')
    f, axs = plt.subplots(5,3,figsize=(15, 15))
    i= -1
    p1 = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == True) &
        (df.loc[:,"period"] == 1)
    )
    p2 = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == True) &
        (df.loc[:,"period"] == 2)
    )
    p3 = (
        (df.loc[:,"team_name"] == teamname) &
        (df.loc[:,"home_game"] == True) &
        (df.loc[:,"period"] == 3)
    )
    x_1 = df.loc[p1,"coordinate_x"]
    y_1 = df.loc[p1,"coordinate_y"]
    x_2 = df.loc[p2,"coordinate_x"]
    y_2 = df.loc[p2,"coordinate_y"]
    x_3 = df.loc[p3,"coordinate_x"]
    y_3 = df.loc[p3,"coordinate_y"]
    plotshotmap(
        base_image,
        -0.5*y_1,
        x_1,axs[i+1,0],
        teamname+' P1 All Shots (n=' + str(len(x_1)) + ")"
        )
    plotshotmap(
        base_image,
        -0.5*y_2,
        x_2,axs[i+1,1],
        teamname+' P2 All Shots (n=' + str(len(x_2)) + ")"
        )
    plotshotmap(
        base_image,
        -0.5*y_3,
        x_3,axs[i+1,2],
        teamname+' P3 Teams All Shots (n=' + str(len(x_3)) + ")"
        )
    shot_types = ["goal","saved","blocked","wide"]
    for i in range(0,len(shot_types)):
        st = shot_types[i]
        p1 = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st) &
            (df.loc[:,"period"] == 1)
        )
        p2 = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st) &
            (df.loc[:,"period"] == 2)
        )
        p3 = (
            (df.loc[:,"team_name"] == teamname) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st) &
            (df.loc[:,"period"] == 3)
        )
        x_1 = df.loc[p1,"coordinate_x"]
        y_1 = df.loc[p1,"coordinate_y"]
        x_2 = df.loc[p2,"coordinate_x"]
        y_2 = df.loc[p2,"coordinate_y"]
        x_3 = df.loc[p3,"coordinate_x"]
        y_3 = df.loc[p3,"coordinate_y"]
        axs[i+1,0].imshow(base_image,extent = (-50,50,0,100))
        sns.kdeplot(
            data=-0.5*y_1,data2=x_1,
            shade=True,
            ax=axs[i+1,0],
            alpha=0.8,
            shade_lowest=False,
            cmap="Reds"
            )
        axs[i+1,0].set_title(
            teamname+' Home P1 ' + st +" (n=" + str(len(x_1)) + ")"
            )
        axs[i+1,1].imshow(base_image,extent = (-50,50,0,100))
        sns.kdeplot(
            data=-0.5*y_2,
            data2=x_2,
            shade=True,
            ax=axs[i+1,1],
            alpha=0.8,
            shade_lowest=False,
            cmap="Reds"
            )
        axs[i+1,1].set_title(
            teamname+' Away P2 ' + st +" (n=" + str(len(x_2)) + ")"
            )
        axs[i+1,2].imshow(base_image,extent = (-50,50,0,100))
        sns.kdeplot(
            data=-0.5*y_3,
            data2=x_3,
            shade=True,
            ax=axs[i+1,2],
            alpha=0.8,
            shade_lowest=False,cmap="Reds"
            )
        axs[i+1,2].set_title(
            teamname+' All P3 ' + st +" (n=" + str(len(x_3)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_1,
            x_1,axs[i+1,0],
            teamname+' P1 ' + st +" (n=" + str(len(x_1)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_2,
            x_2,
            axs[i+1,1],
            teamname+' P2 ' + st +" (n=" + str(len(x_2)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_3,
            x_3,axs[i+1,2],
            teamname+' P3 ' + st +" (n=" + str(len(x_3)) + ")"
            )
    plt.tight_layout();
    
    
def plotplayermaps(df,playername,base_image):
    '''
    A function to generate shot heat maps for shots by a single player.
    5 x 3 plots are generated, the 3 columns relating to shots at home,
    away, and both combined. The 5 rows relating to all shots, goals,
    saved shots, blocked shots, and wide shots

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    playername : String
        The name of the player to plot.
    base_image : numpy.ndarray
        The image of the rink layout

    Raises
    ------
    ValueError
        If an incorrect player name is specified.

    Returns
    -------
    None.

    '''
    if sum(df.loc[:,"fullname"] == playername) < 1:
        raise ValueError('Incorrect player name specified.')
    f, axs = plt.subplots(5,3,figsize=(15, 15))
    i= -1
    home = (
        (df.loc[:,"fullname"] == playername) &
        (df.loc[:,"home_game"] == True)
    )
    away = (
        (df.loc[:,"fullname"] == playername) &
        (df.loc[:,"home_game"] == False)
    )
    x_h = df.loc[home,"coordinate_x"]
    y_h = df.loc[home,"coordinate_y"]
    x_a = df.loc[away,"coordinate_x"]
    y_a = df.loc[away,"coordinate_y"]
    x_ha = x_h.append(-x_a)
    y_ha = y_h.append(-y_a)
    plotshotmap(
        base_image,
        -0.5*y_h,
        x_h,axs[i+1,0],
        playername+' Home All Shots (n=' + str(len(x_h)) + ")"
        )
    plotshotmap(
        base_image,
        0.5*y_a,
        -x_a,
        axs[i+1,1],
        playername+' Away All Shots (n=' + str(len(x_a)) + ")"
        )
    plotshotmap(
        base_image,
        -0.5*y_ha,
        x_ha,axs[i+1,2],
        playername+' H&A Teams All Shots (n=' + str(len(x_ha)) + ")"
        )
    shot_types = ["goal","saved","blocked","wide"]
    for i in range(0,len(shot_types)):
        st = shot_types[i]
        home = (
            (df.loc[:,"fullname"] == playername) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == st)
        )
        away = (
            (df.loc[:,"fullname"] == playername) &
            (df.loc[:,"home_game"] == False) &
            (df.loc[:,"shot_outcome"] == st)
        )
        x_h = df.loc[home,"coordinate_x"]
        y_h = df.loc[home,"coordinate_y"]
        x_a = df.loc[away,"coordinate_x"]
        y_a = df.loc[away,"coordinate_y"]
        x_ha = x_h.append(-x_a)
        y_ha = y_h.append(-y_a)
        plotshotmap(
            base_image,
            -0.5*y_h,
            x_h,axs[i+1,0],
            playername+' Home ' + st +" (n=" + str(len(x_h)) + ")"
            )
        plotshotmap(
            base_image,
            0.5*y_a,
            -x_a,axs[i+1,1],
            playername+' Away ' + st +" (n=" + str(len(x_a)) + ")"
            )
        plotshotmap(
            base_image,
            -0.5*y_ha,
            x_ha,axs[i+1,2],
            playername+' H&A ' + st +" (n=" + str(len(x_ha)) + ")"
            )
    plt.tight_layout();
    
def plotallteamsmaps(df,home,shottype,base_image):
    '''
    A function to generate shot heat maps for shots for all teams.
    2 x 5 plots are generated, the shots maps relating to the shot type
    specified (goal, saved, wide, blocked, all), either home or away games

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    home : boolean
        If True, plot shot maps for home games, else away games
    shottype : string
        The shot type to plot, one of: goal, saved, wide, blocked, all
    base_image : numpy.ndarray
        The image of the rink layout

    Returns
    -------
    None.

    '''
    shottype = shottype.lower()
    f, axs = plt.subplots(2,5,figsize=(15, 8))
    teams = np.sort(df.loc[:,"team_name"].unique())
    for i in range(0,len(teams)):
        if shottype == "all":
            idxs = (
                (df.loc[:,"team_name"] == teams[i]) &
                (df.loc[:,"home_game"] == home)
                )
        else:
            idxs = (
                (df.loc[:,"team_name"] == teams[i]) &
                (df.loc[:,"home_game"] == home) &
                (df.loc[:,"shot_outcome"] == shottype)
                )
        if home:
            x = df.loc[idxs,"coordinate_x"]
            y = -df.loc[idxs,"coordinate_y"]
            title = teams[i]+"\n Home "+shottype+" (n="+str(len(x))+")"
        else:
            x = -df.loc[idxs,"coordinate_x"]
            y = df.loc[idxs,"coordinate_y"] 
            title = teams[i]+"\n Away "+shottype+" (n="+str(len(x))+")"
        if i < 5:
            plotshotmap(base_image,0.5*y,x,axs[0,i],title)
        else:
            plotshotmap(base_image,0.5*y,x,axs[1,i-5],title)
    plt.tight_layout();
    
def plotallteamsmaps_comb(df,home,shottype,base_image):
    '''
    A function to generate shot heat maps for shots for all teams.
    2 x 5 plots are generated, the shots maps relating to the shot type
    specified (goal, saved, wide, blocked, all), combined home and away games.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    shottype : string
        The shot type to plot, one of: goal, saved, wide, blocked
    base_image : numpy.ndarray
        The image of the rink layout

    Returns
    -------
    None.

    '''
    shottype = shottype.lower()
    f, axs = plt.subplots(2,5,figsize=(15, 8))
    teams = np.sort(df.loc[:,"team_name"].unique())
    for i in range(0,len(teams)):
        if shottype == "all":
            idxs = (
            (df.loc[:,"team_name"] == teams[i]) &
            (df.loc[:,"home_game"] == True)
            )
        else:
            idxs = (
            (df.loc[:,"team_name"] == teams[i]) &
            (df.loc[:,"home_game"] == True) &
            (df.loc[:,"shot_outcome"] == shottype)
            )
        x = df.loc[idxs,"coordinate_x"]
        y = -df.loc[idxs,"coordinate_y"]
        title = teams[i] + "\n Home " + shottype + " (n=" + str(len(x)) + ")"
        if shottype == "all":
            idxs = (
            (df.loc[:,"team_name"] == teams[i]) &
            (df.loc[:,"home_game"] == False)
            )
        else:
            idxs = (
            (df.loc[:,"team_name"] == teams[i]) &
            (df.loc[:,"home_game"] == False) &
            (df.loc[:,"shot_outcome"] == shottype)
            )
        x.append(-df.loc[idxs,"coordinate_x"])
        y.append(df.loc[idxs,"coordinate_y"])
        if i < 5:
            plotshotmap(base_image,0.5*y,x,axs[0,i],title)
        else:
            plotshotmap(base_image,0.5*y,x,axs[1,i-5],title)
    plt.tight_layout(); 
    
    
def plotplyrdists(df,teamname,shotbnd = 0):
    '''
    Generate a combined swarm & violin plot of shot distances of players
    for a single team. Goals are highlighted in the plot as solid points

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team to plot.
    shotbnd : int, optional
        Player must have attempted more than shotbnd to plot them.
        The default is 0.

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(15,25))
    inds = (df.loc[:,"team_name"] == teamname)
    df_temp = df.loc[inds,:].copy()
    nshots = df_temp.groupby("fullname", sort=False).count()["id"]
    plyrsbnd = df_temp.groupby(
        "fullname",
        sort=False
        ).count().index[nshots>shotbnd]
    df_temp = df_temp.loc[df_temp.loc[:,"fullname"].isin(plyrsbnd),:]
    sortedplyrnames = df_temp.groupby(
        "fullname",
        sort=False
        ).count().sort_values(by="id", ascending=False).index
    colours = ["#bcbec2","#000000"]
    ax = sns.swarmplot(
        x="shotdistance_m",
        y="fullname",
        hue="goal",
        data=df_temp,
        palette=sns.color_palette(colours),
        dodge=False,
        order = sortedplyrnames
        )
    sns.violinplot(
        x="shotdistance_m",
        y="fullname",
        inner=None,
        data=df_temp,
        order = sortedplyrnames,
        color="grey",ax=ax
        )
    plt.xlim(0,30)

    title = teamname + " Shot Distance Distribution"
    plt.title(title)
    plt.xlabel('Distance (m)')
    plt.tight_layout();
    
def plotplyrdists_ha(df,teamname,home,shotbnd = 0):
    '''
    Generate a combined swarm & violin plot of shot distances of players
    for a single team at home or away.
    Goals are highlighted in the plot as solid points.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team to plot.
    home : boolean
        If True, plot shot maps for home games, else away games.
    shotbnd : int, optional
        Player must have attempted more than shotbnd to plot them.
        The default is 0.

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(15,25))
    inds = (df.loc[:,"team_name"]==teamname)&(df.loc[:,"home_game"]==home)
    df_temp = df.loc[inds,:].copy()
    nshots = df_temp.groupby("fullname", sort=False).count()["id"]
    plyrsbnd = df_temp.groupby(
        "fullname",
        sort=False
        ).count().index[nshots>shotbnd]
    df_temp = df_temp.loc[df_temp.loc[:,"fullname"].isin(plyrsbnd),:]
    sortedplyrnames = df_temp.groupby(
        "fullname",
        sort=False
        ).count().sort_values(by="id", ascending=False).index
    colours = ["#bcbec2","#000000"]
    ax = sns.swarmplot(
        x="shotdistance_m",
        y="fullname",
        hue="goal",
        data=df_temp,
        palette=sns.color_palette(colours),
        dodge=False,
        order = sortedplyrnames
        )
    sns.violinplot(
        x="shotdistance_m",
        y="fullname",
        inner=None,
        data=df_temp,
        order = sortedplyrnames,
        color="grey",ax=ax
        )
    plt.xlim(0,30)
    if home:
        title = teamname + " Shot Distance Distribution, Home Games"
    else:
        title = teamname + " Shot Distance Distribution, Away Games"
    plt.title(title)
    plt.xlabel('Distance (m)')
    plt.ylabel('Player')
    plt.tight_layout();

def plotteamdists_ha(df,home):
    '''
    Generate a combined swarm & violin plot of shot distances of all teams.
    Goals are highlighted in the plot as solid points. Shots are either at
    home or away

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    home : boolean
        If True, plot shot maps for home games, else away games.

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(15,60))
    inds = (df.loc[:,"home_game"] == home)
    df_temp = df.loc[inds,:].copy()
    #sortedteamnames = df_temp.groupby("team_name", sort=False).count().sort_values(by="id", ascending=False).index
    sortedteamnames = df.groupby("team_name", sort=True).count().index
    colours = ["#bcbec2","#000000"]
    ax = sns.swarmplot(
        x="shotdistance_m",
        y="team_name",
        hue="goal",
        data=df_temp,
        palette=sns.color_palette(colours),
        dodge=False,
        order = sortedteamnames
        )
    sns.violinplot(
        x="shotdistance_m",
        y="team_name",
        data=df,
        inner=None,
        order = sortedteamnames,
        palette=sns.color_palette(teamcols),
        ax=ax
        )
    plt.xlim(0,30)
    if home:
        title = "Shot Distance Distribution: All Teams, Home Games"
    else:
        title = "Shot Distance Distribution: All Teams, Away Games"
    plt.title(title)
    plt.xlabel('Distance (m)')
    plt.ylabel('Team')
    plt.tight_layout();
    

def plotteamdists(df):
    '''
    Generate a combined swarm & violin plot of shot distances of all teams.
    Goals are highlighted in the plot as solid points.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(15,100))
    #sortedteamnames = df.groupby("team_name", sort=False).count().sort_values(by="id", ascending=False).index
    sortedteamnames = df.groupby("team_name", sort=True).count().index
    colours = ["#bcbec2","#000000"]
    ax = sns.swarmplot(
        x="shotdistance_m",
        y="team_name",
        hue="home_game",
        data=df,
        palette=sns.color_palette(colours),
        dodge=True,
        order = sortedteamnames
        )
    sns.violinplot(
        x="shotdistance_m",
        y="team_name",
        hue="home_game",
        data=df,
        dodge=True,
        order = sortedteamnames,
        palette=sns.color_palette(teamcols),
        inner=None,
        ax=ax
        )
    plt.xlim(0,30)
    plt.title("Shot Distance Distribution: All Teams")
    plt.xlabel('Distance (m)')
    plt.ylabel('Team')
    plt.tight_layout();
    
def plotsingleteamdists(df,teamname):
    '''
    Generate a combined swarm & violin plot of shot distances of a single
    team. Shots are separated by home and away.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    teamname : String
        The name of the team to plot.
        
    Returns
    -------
    None.

    '''
    plt.figure(figsize=(15,10))
    inds = df.loc[:,"team_name"] == teamname
    df_temp = df.loc[inds,:].copy()
    df_temp.loc[:,"home1"] = 0
    df_temp.loc[df_temp.loc[:,"home_game"]==True,"home1"] = 1
    colours = ["#bcbec2","#000000"]
    ax = sns.swarmplot(
        x="shotdistance_m",
        y="home_game",
        hue="goal",
        data=df_temp,
        palette=sns.color_palette(colours),
        dodge=False,
        orient = "h"
        )
    sns.violinplot(
        x="shotdistance_m",
        y="home_game",
        inner=None,
        data=df_temp,
        orient = "h"
        )
    plt.xlim(0,30)
    plt.yticks([0,1],("Away","Home"))
    plt.title(teamname + " Shot Distance Distribution")
    plt.xlabel('Distance (m)')
    plt.ylabel('Home')
    plt.tight_layout();

def genallteamsmaps(df,home,shottype):
    '''
    A function to generate shot heat maps for shots for all teams.
    The heat maps are not plotted but are returned in an array

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the shot data
    home : boolean
        If True, plot shot maps for home games, else away games
    shottype : string
        The shot type to plot, one of: goal, saved, wide, blocked, all

    Returns
    -------
    shotmaps : numpy.ndarray
        Array containing shot maps defined on a numpy.mgrid.

    '''
    shotmaps = np.zeros([101,101,10])
    shottype = shottype.lower()
    teams = np.sort(df.loc[:,"team_name"].unique())
    xx, yy = np.mgrid[-50:51,0:101]
    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    for i in range(0,len(teams)):
        if shottype == "all":
            idxs = (
                (df.loc[:,"team_name"] == teams[i]) &
                (df.loc[:,"home_game"] == home)
                )
        else:
            idxs = (
                (df.loc[:,"team_name"] == teams[i]) &
                (df.loc[:,"home_game"] == home) &
                (df.loc[:,"shot_outcome"] == shottype)
                )
        if home:
            x = df.loc[idxs,"coordinate_x"]
            y = -df.loc[idxs,"coordinate_y"]
        else:
            x = -df.loc[idxs,"coordinate_x"]
            y = df.loc[idxs,"coordinate_y"]
        xy_train  = np.vstack([x, 0.5*y]).T
        kde = stats.gaussian_kde(xy_train.T,bw_method="scott")
        shotmaps[:,:,i] = (kde(xy_sample.T).reshape(xx.shape))
    return shotmaps

