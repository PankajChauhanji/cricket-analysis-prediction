def get_teams_array(team):
    temp_array = []
    team_array = ['CSK', 'DD', 'KXP', 'KKR', 'MI', 'RR', 'RCB', 'SRH']
    for i in range(len(temp_array)):
        temp_array.append(1 if (team == team_array[i]) else 0)
    return temp_array