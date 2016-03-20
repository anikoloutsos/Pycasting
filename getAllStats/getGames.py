import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

year = 2015

teams = pd.read_csv('teams.csv')
teamsName = 'name'
teamsPrefix1 = 'prefix_1'
teamsPrefix2 = 'prefix_2'

BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'
BASE_GAME_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'

game_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
for index, row in teams.iterrows():
    team = row[teamsName]
    print("Getting info on: " + team)
	
    r = requests.get(BASE_URL.format(row[teamsPrefix1], year, row[teamsPrefix2]))
    table = BeautifulSoup(r.text,'html.parser').table
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        try: 
            id = columns[2].a['href'].split('?id=')[1]
            home = True if columns[1].li.text == 'vs' else False
            other_team = columns[1].find_all('a')[1]['href']
            other_team = other_team.split('/')[-1:][0]
            other_team = teams['name'][teams['prefix_2'] == other_team]
            other_team = other_team.values[0]
            score = columns[2].a.text.split(' ')[0].split('-')
            won = True if columns[2].span.text == 'W' else False

            game_id.append(id)
            home_team.append(team if home else other_team)
            visit_team.append(team if not home else other_team)
            d = datetime.strptime(columns[0].text, '%a, %b %d')
            dates.append(date(year, d.month, d.day))
            
            if home:
                if won:
                    home_team_score.append(score[0])
                    visit_team_score.append(score[1])
                else:
                    home_team_score.append(score[1])
                    visit_team_score.append(score[0])
            else:
                if won:
                    home_team_score.append(score[1])
                    visit_team_score.append(score[0])
                else:
                    home_team_score.append(score[0])
                    visit_team_score.append(score[1])

            # Extra stats
            # r = requests.get(BASE_GAME_URL.format(id))
            # table = BeautifulSoup(r.text).find('table', class_='mod-data')
            # heads = table.find_all('thead')
            # bodies = table.find_all('tbody')
            # # print(heads)
            # headers = heads[2].tr.find_all('th')[2:]
            # headers = [th.text for th in headers]
            # headers[3] = headers[3].split('\n')[0]
            # del headers[-2]
            # visit_stats = bodies[2].tr.find_all('td')[1:]
            # visit_stats = [td.text for td in visit_stats]
            # del visit_stats[-2]
            # print(headers)
            # print(visit_stats)

        except Exception as e:
            pass # Not all columns row are a game, is OK
            # print(e)

dic = {'id': game_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team, 
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}
        

		
games = pd.DataFrame(dic).drop_duplicates(subset='id').set_index('id')
f = open('games.csv','wt')
f.write(games.to_csv())
f.close