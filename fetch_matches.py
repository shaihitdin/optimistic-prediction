from bs4 import BeautifulSoup
import requests


link = 'https://www.goal.com/en/news/premier-league-2018-19-full-fixture-list-gameweek-1-to-38/o3arezke46t11whpdl1yl0nyi'


info_file = open("unformatted_matches.txt", "r")

match_order_per_team = dict()


for i in range(38):
    info_file.readline()
    info_file.readline()
    for j in range(10):
        match = info_file.readline()
        match_elements = match.split()
        if match_elements[2] not in match_order_per_team:
            match_order_per_team[match_elements[2]] = list()
        if match_elements[4] not in match_order_per_team:
            match_order_per_team[match_elements[4]] = list()
        match_order_per_team[match_elements[2]].append(match_elements[4])
        match_order_per_team[match_elements[4]].append(match_elements[2])


res_file = open('formatted_matches.txt', 'w')

for team, games in match_order_per_team.items():
    print(team, end=' ', file=res_file)
    for rival in games:
        print(rival, end=' ', file=res_file)
    print('', file=res_file)
