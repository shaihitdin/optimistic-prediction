
actual_position = dict()
actual_score = dict()
predicted_score = dict()
predicted_position = dict()

with open('club_true_standings.txt', 'r') as standings_file:
    for line in standings_file:
        position, club_name, pts, _ = line.split()
        actual_position[club_name] = int(position)
        actual_score[club_name] = int(pts)

with open('predicted_scores.txt', 'r') as predictions_file:
    predict_standings = []
    for line in predictions_file:
        club_name, pts = line.split()
        predicted_score[club_name] = float(pts)
        predict_standings.append((pts, club_name))
    predict_standings = sorted(predict_standings, key=lambda x: x[0])
    predict_standings.reverse()
    for i in range(len(predict_standings)):
        predicted_position[predict_standings[i][1]] = i + 1

sum_of_score_diff = 0
quadratic_sum_of_score_diff = 0
sum_of_position_diff = 0
quadratic_sum_of_position_diff = 0

for club_name in actual_score.keys():
    sum_of_score_diff += abs(actual_score[club_name] - predicted_score[club_name])
    quadratic_sum_of_score_diff += abs(actual_score[club_name] - predicted_score[club_name]) ** 2
    sum_of_position_diff += abs(predicted_position[club_name] - actual_position[club_name])
    quadratic_sum_of_position_diff += abs(predicted_position[club_name] - actual_position[club_name]) ** 2

print("SUM OF SCORE DIFFIRENCE: {} AVERAGE SCORE DIFFERENCE: {}".format(sum_of_score_diff, sum_of_score_diff / 20))
print("QUADRATIC SUM OF SCORE DIFFIRENCE: {} AVERAGE QUADRATIC SUM OF SCORE DIFFIRENCE: {}".format(quadratic_sum_of_score_diff, quadratic_sum_of_score_diff / 20))
print("SUM OF POSITION DIFFIRENCE: {} AVERAGE POSITION DIFFERENCE: {}".format(sum_of_position_diff, sum_of_position_diff / 20))
print("QUADRATIC SUM OF POSITION DIFFIRENCE: {} AVERAGE QUADRATIC SUM OF POSITION DIFFIRENCE: {}".format(quadratic_sum_of_position_diff, quadratic_sum_of_position_diff / 20))
