import pickle
import numpy as np
def get_regressor():
    # Load the Random Forest CLassifier model
    regressor = pickle.load(open('src/first-innings-score-lr-model.pkl', 'rb'))
    return regressor

def predict_final_score(request):
    # To predict the final score.
    temp_array = list()
    batting_team = request.form['batting-team']
    bowling_team = request.form['bowling-team']
    venue = request.form['venue']
    team_array = ['CSK', 'DD', 'KXP', 'KKR', 'MI', 'RR', 'RCB', 'SRH']
    temp_array = [ 1 if batting_team == team_array[i] else 0 for i in range(len(team_array))]
    print(temp_array)

    temp_array += [ 1 if bowling_team == team_array[i] else 0 for i in range(len(team_array))]
    print('now', temp_array)
        
    overs = float(request.form['overs'])
    runs = int(request.form['runs'])
    wickets = int(request.form['wickets'])
    runs_in_prev_5 = int(request.form['runs_in_prev_5'])
    wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
    
    temp_array += [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
    
    data = np.array([temp_array])
    regressor = get_regressor()
    final_score = int(regressor.predict(data)[0])
    return final_score
