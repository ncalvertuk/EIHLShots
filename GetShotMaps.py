#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:45:09 2020

@author: ncalvertuk
"""

import re
import requests
import time

fixtures_url = "https://www.eliteleague.co.uk/schedule?id_season=2&id_team=0&id_month=999"
fixtures_http = requests.get(fixtures_url)
idxs = [m.start() for m in re.finditer("a href=\"/game/", fixtures_http.text)]
game_ids = []
for ind in idxs:
    ind1 = fixtures_http.text.find(" class",ind)
    g_id = fixtures_http.text[ind+8:ind1-1]
    
    track_url = "https://www.eliteleague.co.uk" +g_id + "/tracking"
    track_http = requests.get(track_url)
    ind2 = track_http.text.find("https://eihl.hokejovyzapis.cz/visualization/")
    ind3 = track_http.text.find("\"",ind2)
    s_id = track_http.text[(ind3-4):ind3]
    if(s_id[0] == "="):
        s_id = s_id[1:]
    print(g_id)
    print(s_id)
    if s_id not in game_ids:
        game_ids.append(int(s_id))
        json_url = "https://s3-eu-west-1.amazonaws.com/eihl.hokejovyzapis.cz/visualization/shots/" + str(s_id) + ".json"
        txt = requests.get(json_url).text
        file_name = str(s_id) + ".json"
        with open(file_name, 'w') as f:
            f.write(txt)
    time.sleep(10)

    
