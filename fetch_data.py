from bs4 import BeautifulSoup
import requests


club_links = [
    'https://www.transfermarkt.com/manchester-city/startseite/verein/281/saison_id/2018',
    'https://www.transfermarkt.com/fc-chelsea/startseite/verein/631/saison_id/2018',
    'https://www.transfermarkt.com/fc-liverpool/startseite/verein/31/saison_id/2018',
    'https://www.transfermarkt.com/manchester-united/startseite/verein/985/saison_id/2018',
    'https://www.transfermarkt.com/tottenham-hotspur/startseite/verein/148/saison_id/2018',
    'https://www.transfermarkt.com/fc-arsenal/startseite/verein/11/saison_id/2018',
    'https://www.transfermarkt.com/fc-everton/startseite/verein/29/saison_id/2018',
    'https://www.transfermarkt.com/leicester-city/startseite/verein/1003/saison_id/2018',
    'https://www.transfermarkt.com/west-ham-united/startseite/verein/379/saison_id/2018',
    'https://www.transfermarkt.com/fc-southampton/startseite/verein/180/saison_id/2018',
    'https://www.transfermarkt.com/crystal-palace/startseite/verein/873/saison_id/2018',
    'https://www.transfermarkt.com/fc-fulham/startseite/verein/931/saison_id/2018',
    'https://www.transfermarkt.com/newcastle-united/startseite/verein/762/saison_id/2018',
    'https://www.transfermarkt.com/fc-burnley/startseite/verein/1132/saison_id/2018',
    'https://www.transfermarkt.com/afc-bournemouth/startseite/verein/989/saison_id/2018',
    'https://www.transfermarkt.com/brighton-amp-hove-albion/startseite/verein/1237/saison_id/2018',
    'https://www.transfermarkt.com/fc-watford/startseite/verein/1010/saison_id/2018',
    'https://www.transfermarkt.com/wolverhampton-wanderers/startseite/verein/543/saison_id/2018',
    'https://www.transfermarkt.com/huddersfield-town/startseite/verein/1110/saison_id/2018',
    'https://www.transfermarkt.com/cardiff-city/startseite/verein/603/saison_id/2018'
]


def info_to_class(type_, player_info):
    player_number = player_info.find(class_='rn_nummer').contents[0]
    player_cost_str = player_info.find(class_='rechts hauptlink').contents[0]
    if not player_number.isnumeric():
        return None
    if '€' not in player_cost_str:
        return None
    player_cost_str = player_cost_str.replace('€', '')
    player_cost = 0
    if 'Th.' in player_cost_str:
        player_cost_str = player_cost_str.replace('Th.', '')
        player_cost = int(float(player_cost_str) * 1000)
    elif 'm' in player_cost_str:
        player_cost_str = player_cost_str.replace('m', '')
        player_cost = int(float(player_cost_str) * 1000000)
    else:
        raise ValueError(player_cost_str)
    return type_, player_number, player_cost


info_file = open("info_club.txt", "w")

for club in club_links:
    r = requests.get(club, headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
    soup = BeautifulSoup(r.text, 'html.parser')
    team_name = ""
    team_title = soup.title.contents[0].split()
    for s in team_title:
        if s == '-':
            team_name = team_name[:len(team_name) - 1]
            break
        team_name += s
        team_name += "_"


    player_arr = []

    for player in soup.find_all(title='Torwart'):
        player_info = player.parent
        player_tuple = info_to_class(0, player_info)
        if not player_tuple:
            continue
        player_arr.append(player_tuple)

    for player in soup.find_all(title='Abwehr'):
        player_info = player.parent
        player_tuple = info_to_class(1, player_info)
        if not player_tuple:
            continue
        player_arr.append(player_tuple)

    for player in soup.find_all(title='Mittelfeld'):
        player_info = player.parent
        player_tuple = info_to_class(2, player_info)
        if not player_tuple:
            continue
        player_arr.append(player_tuple)

    for player in soup.find_all(title='Sturm'):
        player_info = player.parent
        player_tuple = info_to_class(3, player_info)
        if not player_tuple:
            continue
        player_arr.append(player_tuple)

    print(team_name, len(player_arr), file=info_file)
    for player in player_arr:
        print(player[1], player[0], player[2], file=info_file)


info_file.close()


