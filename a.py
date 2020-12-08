import pulp
import numpy as np
import math

info_file = open('info.txt', 'r')


MAX_MARKET_VALUE = 222000000
COEFF = 100 / math.log(MAX_MARKET_VALUE)

class Player:
    def __init__(self, player_number, player_type, player_rank):
        self.player_number = player_number
        self.player_type = player_type
        self.player_rank = player_rank

class Club:
    def __init__(self, club_name, players):
        self.club_name = club_name
        self.players = players




def club_to_rating(club):
    prob = pulp.LpProblem('{}_rating'.format(club.club_name), pulp.LpMaximize)
    # decision variables
    starting11 = [
        pulp.LpVariable('x_{}_start'.format(i), 0, 1, cat='Integer')
        for i in range(len(club.players))
    ]
    sub3 = [
        pulp.LpVariable('x_{}_sub'.format(i), 0, 1, cat='Integer')
        for i in range(len(club.players))
    ]

    # objective function
    prob += sum(starting11[i] * club.players[i].player_rank + sub3[i] * (club.players[i].player_rank / 3) for i in range(len(club.players)))

    # starting11 and sub3 size
    prob += sum(starting11) == 11
    prob += sum(sub3) == 3

    # can't be both in starting11 and sub3
    for i in range(len(club.players)):
        prob += (starting11[i] + sub3[i]) <= 1
    
    # 1 goalkeeper
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 0) == 1
    # 1 goalkeeper
    prob += sum(starting11[i] + sub3[i] for i in range(len(club.players)) if club.players[i].player_type == 0) == 1
    
    # 3-5 defenders
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 1) <= 5
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 1) >= 3

    # <= 5 defenders
    prob += sum(starting11[i] + sub3[i] for i in range(len(club.players)) if club.players[i].player_type == 1) <= 5

    # 3-5 midfielders
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 2) <= 5
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 2) >= 3

    # <= 5 midfielders
    prob += sum(starting11[i] + sub3[i] for i in range(len(club.players)) if club.players[i].player_type == 2) <= 5

    # 1-3 attackers
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 3) <= 3
    prob += sum(starting11[i] for i in range(len(club.players)) if club.players[i].player_type == 3) >= 1

    # <= 3 attackers
    prob += sum(starting11[i] + sub3[i] for i in range(len(club.players)) if club.players[i].player_type == 3) <= 3


    prob.solve()

    return pulp.value(prob.objective)

def getScore(club_name, club_rating):

    match_opponent_rating = []


    with open('formatted_matches.txt', 'r') as matches_file:
        for line in matches_file:
            order_of_matches = line.split()
            if order_of_matches[0] == club_name:
                for i in range(1, len(order_of_matches)):
                    for j in range(len(club_rating)):
                        if club_rating[j][1].club_name == order_of_matches[i]:
                            match_opponent_rating.append(club_rating[j][0])


    for j in range(len(club_rating)):
        if club_rating[j][1].club_name == club_name:
            club = club_rating[j][1]

    prob = pulp.LpProblem('{}_score'.format(club.club_name), pulp.LpMaximize)

    starting11_arr = []
    sub3_arr = []
    #squad_rating_arr = []

    obj_func = None

    for match_num in range(len(match_opponent_rating)):
        starting11_arr.append([
            pulp.LpVariable('x_{}_{}_start'.format(match_num, i), 0, 1, cat='Integer')
            for i in range(len(club.players))
        ])
        sub3_arr.append([
            pulp.LpVariable('x_{}_{}_sub'.format(match_num, i), 0, 1, cat='Integer')
            for i in range(len(club.players))
        ])
        #squad_rating = pulp.LpVariable('game_{}_pos'.format(match_num), 0)

        # starting11 and sub3 size
        prob += sum(starting11_arr[match_num]) == 11
        prob += sum(sub3_arr[match_num]) <= 3

        # can't be both in starting11 and sub3
        for i in range(len(club.players)):
            prob += (starting11_arr[match_num][i] + sub3_arr[match_num][i]) <= 1
        
        # 1 goalkeeper
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 0) == 1
        # 1 goalkeeper
        prob += sum(starting11_arr[match_num][i] + sub3_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 0) == 1
        
        # 3-5 defenders
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 1) <= 5
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 1) >= 3

        # <= 5 defenders
        prob += sum(starting11_arr[match_num][i] + sub3_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 1) <= 5

        # 3-5 midfielders
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 2) <= 5
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 2) >= 3

        # <= 5 midfielders
        prob += sum(starting11_arr[match_num][i] + sub3_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 2) <= 5

        # 1-3 attackers
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 3) <= 3
        prob += sum(starting11_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 3) >= 1

        # <= 3 attackers
        prob += sum(starting11_arr[match_num][i] + sub3_arr[match_num][i] for i in range(len(club.players)) if club.players[i].player_type == 3) <= 3


        x = sum(starting11_arr[match_num][i] * club.players[i].player_rank + sub3_arr[match_num][i] * (club.players[i].player_rank / 3) for i in range(len(club.players)))
        if not obj_func:
            obj_func = x
        else:
            obj_func = obj_func + x
        if match_num >= 5:
            # fatigue
            for i in range(len(club.players)):
                prob += starting11_arr[match_num-5][i] + sub3_arr[match_num-5][i] * 0.33 + starting11_arr[match_num-4][i] + sub3_arr[match_num-4][i] * 0.33 + starting11_arr[match_num-3][i] + sub3_arr[match_num-3][i] * 0.33 + starting11_arr[match_num-2][i] + sub3_arr[match_num-2][i] * 0.33 + starting11_arr[match_num-1][i] + sub3_arr[match_num-1][i] * 0.33 + starting11_arr[match_num][i] + sub3_arr[match_num][i] * 0.33 <= 4

    #print(obj_func)

    prob += obj_func

    prob.solve(pulp.getSolver('PULP_CBC_CMD', timeLimit=60))
    print(pulp.value(prob.objective), sum(match_opponent_rating))

    return 3 * (0.5 * 38 + 0.001 * (pulp.value(prob.objective) - 0.99 * sum(match_opponent_rating)))

club_list = []

with open('info.txt', 'r') as info_file:
    for club_cnt in range(20):
        club_name, player_cnt_str = info_file.readline().split()
        player_cnt = int(player_cnt_str)
        player_list = []
        for i in range(player_cnt):
            player_num_str, player_type_str, player_cost_str = info_file.readline().split()
            player_num = int(player_num_str)
            player_type = int(player_type_str)
            player_cost = int(player_cost_str)
            player_rank = COEFF * math.log(player_cost)

            player_list.append(Player(player_num, player_type, player_rank))

        club_list.append(Club(club_name, player_list))


sum_rating = 0
avg_rating = 0
multiplier = 0

with open('club_rank.txt', 'w') as club_rank_file:

    club_rating = []

    for club in club_list:
        club_rating.append((club_to_rating(club), club))

    club_rating = sorted(club_rating, key=lambda x: x[0])
    club_rating.reverse()

    for rating, club in club_rating:
        sum_rating += rating
        print(rating, club.club_name, file=club_rank_file)

    avg_rating = sum_rating / 20
    multiplier = 1500 / avg_rating


with open('new_club_rank.txt', 'w') as new_club_rank_file:

    for club in club_list:
        for player in club.players:
            player.player_rank = player.player_rank * multiplier

    club_rating = []

    for club in club_list:
        tmp_tuple = (club_to_rating(club), club)
        club_rating.append(tmp_tuple)
        print(tmp_tuple[0], tmp_tuple[1].club_name, file=new_club_rank_file)

    club_rating = sorted(club_rating, key=lambda x: x[0])
    club_rating.reverse()


    new_club_rank_file.close()




with open('predicted_scores.txt', 'w') as prediction_file:
    for club in club_rating:
        print(club[1].club_name, getScore(club[1].club_name, club_rating), file=prediction_file)

