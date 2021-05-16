# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
from util import *

# Load the Random Forest CLassifier model
filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
        bowling_team = request.form['bowling-team']
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
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)



if __name__ == '__main__':
	app.run(debug=True)