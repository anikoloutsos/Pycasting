# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

def get_players(players, team_name):
	array = np.zeros((len(players), len(headers)+1), dtype=object)
	array[:] = np.nan
	for i, player in enumerate(players):
		cols = player.find_all('td')
		array[i, 0] = cols[0].text.split(',')[0]
		if (len(cols) < len(headers)):
			for j in range(1, len(cols)):
				if not cols[1].text.startswith('DNP'):
					array[i, j] = cols[j].text
		else:
			for j in range(1, len(headers) + 1):
				if not cols[1].text.startswith('DNP'):
					array[i, j] = cols[j].text
	#DataFrame = DataFrame.decode('cp-737')
	frame = pd.DataFrame(columns=columns)
	for x in array:
		line = np.concatenate(([index, team_name], x)).reshape(1,len(columns))
		new = pd.DataFrame(line, columns=frame.columns)
		frame = frame.append(new)
		
	return frame




games = pd.read_csv('games.csv')
BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
request = requests.get(BASE_URL.format(games.id[0]))
table = BeautifulSoup(request.text,'html.parser').find('table', class_='mod-data')
heads = table.find_all('thead')
headers = heads[0].find_all('tr')[0].find_all('th')[1:]
headers = [th.text for th in headers]
columns = ['id', 'team', 'player'] + headers
print (headers)
players = pd.DataFrame(columns=columns)



for index, row in games[:3].iterrows():
# for index, row in games.iterrows():
	
	request = requests.get(BASE_URL.format(games.id[index]))
	table = BeautifulSoup(request.text,'html.parser')#.find('table', class_='mod-data')
	heads = table.find_all('thead')
	bodies = table.find_all('tbody')
	
	
	team_1 = heads[0].th.text
	team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
	team_1_players = get_players(team_1_players, team_1)
	print (team_1_players)
	players = players.append(team_1_players)
	
	team_2 = heads[3].th.text
	team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
	team_2_players = get_players(team_2_players, team_2)
	players = players.append(team_2_players)

	
players = players.set_index('id')
#copper.save(players, 'players')
f = open('players.csv','wt')
f.write(players.to_csv())
f.close